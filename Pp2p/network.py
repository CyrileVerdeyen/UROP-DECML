## Code addapted from https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html
## Author: Cyrile Verdeyen

import json
from time import time
from datetime import datetime
import random

from twisted.internet import reactor
from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint,
                                        connectProtocol)
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
import numpy as np

from crypto import generate_nodeid


PING_INTERVAL = 30.0 # Interval for pinging
PEERS_INTERVAL = 180.0 # Interval for asking again for peers
RESPONSE_INTERVAL = 5.0 # Interval for sending responses to questions

def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))

## The factory class houses all the different protocols that each node has, as well as any other constant data.
class PPFactory(Factory):
    def __init__(self, ml):
        self.ml = ml
        pass

    def startFactory(self):
        self.peers = {}
        self.nodeid = generate_nodeid()[:10]
        _print(" [ ] Node ID is: ", self.nodeid)
        self.numProtocols = 0
        self.answeredQuestions = []
        self.questions = {}

    def stopFactory(self):
        pass

    def buildProtocol(self, addr):
        return PPProtocol(self, "HELLO", "LISTENER")

## The PPProtocol is where the communication happens between each of the nodes. This handles the sending, recieving and handling of the data.
class PPProtocol(Protocol):
    def __init__(self, factory, state="HELLO", kind="LISTENER", type="NODE"):
        self.factory = factory
        self.state = state
        self.VERSION = 0
        self.kind = kind
        self.type = type
        self.remote_nodeid = None
        self.remote_type = None
        self.nodeid = self.factory.nodeid
        self.lc_ping = LoopingCall(self.send_ping)
        self.lc_peers = LoopingCall(self.send_addr)
        self.lc_response = LoopingCall(self.send_response)
        self.lastping = None
        self.lastpong = None
        self.sentResponse = []

    def write(self, line):
        self.transport.write((line + "\n").encode('utf-8'))

    def print_peers(self):
        if len(self.factory.peers) == 0:
            _print(" [!] PEERS: No peers connected.")
        else:
            _print(" [ ] PEERS:")
            for peer in self.factory.peers:
                addr, kind = self.factory.peers[peer][:2]
            print(" [*]", peer, "at", addr, kind)

    # This method gets called everytime a connection gets made to a node.
    def connectionMade(self):
        remote_ip = self.transport.getPeer()
        host_ip = self.transport.getHost()
        self.remote_ip = remote_ip.host + ":" + str(remote_ip.port)
        self.host_ip = host_ip.host + ":" + str(host_ip.port)
        self.factory.numProtocols = self.factory.numProtocols + 1
        _print (" [*] Connection from", self.transport.getPeer(), " Number of connections: ", self.factory.numProtocols)

    # This gets called everytime a node dissconects.
    def connectionLost(self, reason):
        if self.remote_nodeid in self.factory.peers:
            self.factory.peers.pop(self.remote_nodeid)
            try: self.lc_ping.stop()
            except AssertionError: pass
        self.factory.numProtocols = self.factory.numProtocols - 1
        _print (" [X] A Node dissconected. Connections left ", self.factory.numProtocols)

    # dataRecieved gets called everytime new bytes arrive at the port that is being listened to.
    def dataReceived(self, data):
        for line in (data.splitlines()):
            line = line.strip()
            msgtype = json.loads(line)['msgtype']
            if self.state in ["HELLO", "SENTHELLO"]:
                # Force first message to be HELLO or crash
                if msgtype == 'hello':
                    self.handle_hello(line)
                else:
                    _print(" [!] Ignoring", msgtype, "in", self.state)
                self.state = "READY"
            elif msgtype == "ping":
                self.handle_ping()
            elif msgtype == "pong":
                self.handle_pong()
            elif msgtype == "addr":
                self.handle_addr(line)
            elif msgtype == "question":
                self.handle_question(line)

    # The first message that gets sent
    def send_hello(self):
        hello = json.dumps({'nodeid': self.nodeid, 'msgtype': 'hello', 'type': 'NODE'})
        self.write(hello)
        self.state = "SENTHELLO"

    # Ping pongs are used to verify the excistance of nodes, and making sure that they have not disconected.
    def send_ping(self):
        ping = json.dumps({'msgtype': 'ping'})
        self.lastping = time()
        _print (" [>] PING to ", self.remote_nodeid, " at ", self.remote_ip)
        self.write(ping)

    def send_pong(self):
        pong = json.dumps({'msgtype': 'pong'})
        self.write(pong)

    def handle_ping(self):
        self.send_pong()

    def handle_pong(self):
        _print (" [<] Got pong from ", self.remote_nodeid, " at ", self.remote_ip)
        ### Update the timestamp
        self.lastpong = time()
        addr, kind = self.factory.peers[self.remote_nodeid][:2]
        self.factory.peers[self.remote_nodeid] = (addr, kind, (self.lastpong - self.lastping))

    # Send the addresses to other nodes and own node
    def send_addr(self):
        peers = self.factory.peers
        listeners = [(n, peers[n][0], peers[n][1])
                    for n in peers]

        addr = json.dumps({'msgtype': 'addr', 'nodes': listeners})
        self.write(addr)

    # Handle the addresses that get sent by other nodes, and contact them if new
    def handle_addr(self, addr):
        json1 = json.loads(addr)
        for node in json1["nodes"]:
            _print(" [*] Recieved Node: "  + node[0] + " " + node[1] + " " + node[2])
            if node[0] == self.nodeid:
                _print(" [!] Not connecting to " + node[0] + ": thats me!")
                continue
            if node[2] == "SPEAKER":
                _print(" [!] Not connecting to " + node[0] + ": is " + node[2])
                continue
            if node[0] in self.factory.peers:
                _print(" [!] Not connecting to " + node[0]  + ": already connected")
                continue
            _print(" [ ] Trying to connect to peer " + node[0] + " " + node[1])
            host, port = node[1].split(":")
            point = TCP4ClientEndpoint(reactor, host, int(port))
            d = connectProtocol(point, PPProtocol(self.factory, "HELLO", "SPEAKER"))
            d.addCallback(gotProtocol)

    def handle_getaddr(self, getaddr):
        self.send_addr()

    def handle_question(self, question):
        message = json.loads(question)
        answers = []
        IDS = []

        _print(" [<] Got question: " , message["questionID"], " from: ", self.remote_nodeid, self.remote_ip)

        if message["questionID"] not in self.factory.answeredQuestions: # If I have not ye answered this
            question = np.asarray(message["question"]).reshape(1, -1)
            answer = self.factory.ml.classify(question)

            _print( " [ ] Response to " ,  message["questionID"], " is ", answer)

            if message["answer"]: # If the message has other answers already
                answers = message["answer"]
                answers.append(answer)
            else:
                answers = [answer]

            if message["IDS"]: # If the message has IDS of nodes that have responded, add own ID to it
                IDS = message["IDS"]
                IDS.append(self.nodeid)

            else:
                IDS = [self.nodeid]

            self.factory.answeredQuestions.append(message["questionID"])
            self.factory.questions[message["questionID"]] = (message["questionID"], message["question"], answers, IDS)

        else:
            _print(" [!] Answered question ",  message["questionID"], " already. Appending differance and sending again.")
            answers = self.factory.questions[message["questionID"]][2]
            IDS = self.factory.questions[message["questionID"]][3]

            for answer in message["answer"]:
                if answer not in answers:
                    answers.append(answer)

            for ID in message["IDS"]:
                if ID not in IDS:
                    IDS.append(ID)

            self.factory.questions[message["questionID"]] = (message["questionID"], message["question"], answers, IDS)
            if message["questionID"] in self.sentResponse:
                self.sentResponse.remove(message["questionID"])


    def send_response(self):
        if self.factory.questions: # If there are questions
            for response, info in self.factory.questions.items(): # For each question in the question log
                notAnswered = []
                for peer, peerInfo in self.factory.peers.items(): # For all peers we are connected too
                    if peerInfo[1] is not "CO": # If the peer is a Node
                        if peer not in info[3]: # If peer has not yet answered
                            notAnswered.append(peer)

                if notAnswered:
                    for node in notAnswered:
                        if info[0] not in self.sentResponse: # If we have not yet sent this reponse yet
                            if self.remote_nodeid == node:
                                message = json.dumps({'msgtype': 'question', 'questionID': info[0], 'question': info[1], 'answer': info[2], 'IDS': info[3]})
                                _print(" [>] Sending: question, to: ", self.remote_nodeid, self.remote_ip)
                                self.sentResponse.append(info[0])
                                self.write(message)
                else:
                    if self.remote_type == "CO":
                        if info[0] not in self.sentResponse:
                            message = json.dumps({'msgtype': 'response', 'questionID': info[0], 'question': info[1], 'answer': info[2], 'IDS': info[3]})
                            _print(" [>] Sending: response, to: ", self.remote_nodeid, self.remote_ip)
                            self.sentResponse.append(info[0])
                            self.write(message)


    # Handle the first message that gets sent
    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_nodeid = hello["nodeid"]
        self.remote_type = hello["type"]
        _print(" [<] Got hello from: " , self.remote_nodeid, self.remote_ip)

        if self.remote_nodeid == self.nodeid:
            _print (" [!] Connected to myself.")
            self.transport.loseConnection()
        else:
            if self.remote_type == "NODE":
                if self.state == "HELLO" :
                    self.add_peer("SPEAKER")
                elif self.state == "SENTHELLO":
                    self.add_peer("LISTENER")
            else:
                self.add_peer("CO")

            self.send_hello()

            _print(" [ ] Starting pinger to " + self.remote_nodeid)
            self.lc_ping.start(PING_INTERVAL, now=True)
            self.lc_peers.start(PEERS_INTERVAL, now=False)
            self.lc_response.start(RESPONSE_INTERVAL, now=True)

            if self.kind == "LISTENER":
                # Tell new audience about my peers
                self.send_addr()

    def add_peer(self, kind):
        entry = (self.remote_ip, kind)
        self.factory.peers[self.remote_nodeid] = entry

def gotProtocol(p):
    """The callback to start the protocol exchange. We let connecting
    nodes start the hello handshake"""
    p.send_hello()