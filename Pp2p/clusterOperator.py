## Author: Cyrile Verdeyen

import json
import itertools
from time import time
from datetime import datetime

from twisted.internet import reactor
from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint,
                                        connectProtocol)
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall

from crypto import generate_nodeid

QUESTION_INTERVAL = 10.0 #How often we send out questions

def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))

## The factory class houses all the different protocols that each node has, as well as any other constant data.
class COFactory(Factory):
    def __init__(self):
        pass

    def startFactory(self):
        self.peers = {}
        self.nodeid = generate_nodeid()[:10]
        self.numProtocols = 0
        self.questions = {}
        self.questionID = 0

    def stopFactory(self):
        pass

    def buildProtocol(self, addr):
        return COProtocol(self, "HELLO", "LISTENER", "OPERATOR")

## The PPProtocol is where the communication happens between each of the nodes. This handles the sending, recieving and handling of the data.
class COProtocol(Protocol):
    def __init__(self, factory, state="HELLO", kind="LISTENER", type="OPERATOR"):
        self.factory = factory
        self.state = state
        self.VERSION = 0
        self.kind = kind
        self.type = type
        self.remote_nodeid = None
        self.nodeid = self.factory.nodeid
        self.lc_question = LoopingCall(self.send_question)
        self.lastQuestion = 0

    def write(self, line):
        self.transport.write((line + "\n").encode('utf-8'))

    def print_peers(self):
        if len(self.factory.peers) == 0:
            _print(" [!] PEERS: No peers connected.")
        else:
            _print(" [ ] PEERS:")
            for peer in self.factory.peers:
                addr, kind = self.factory.peers[peer][:2]
            _print(" [*]", peer, "at", addr, kind)

    # This method gets called everytime a connection gets made to a node.
    def connectionMade(self):
        remote_ip = self.transport.getPeer()
        host_ip = self.transport.getHost()
        self.remote_ip = remote_ip.host + ":" + str(remote_ip.port)
        self.host_ip = host_ip.host + ":" + str(host_ip.port)
        self.factory.numProtocols = self.factory.numProtocols + 1
        print (" [*] Connection from", self.transport.getPeer(), " Number of connections: ", self.factory.numProtocols)

    # This gets called everytime a node dissconects.
    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1
        print (" [X] Node ", self.remote_ip, " dissconected. Connections left ", self.factory.numProtocols)

    # dataRecieved gets called everytime new bytes arrive at the port that is being listened to.
    def dataReceived(self, data):
        for line in (data.splitlines()):
            line = line.strip()
            msgtype = json.loads(line)['msgtype']
            if self.state in ["HELLO", "SENTHELLO"]:
                # Force first message to be HELLO or crash
                if msgtype == 'hello':
                    self.handle_hello(line)
                elif msgtype == 'question':
                    self.handle_question(line)
                else:
                    _print(" [!] Ignoring", msgtype, "in", self.state)
                self.state = "READY"
            elif msgtype == 'ping':
                self.handle_ping
            elif msgtype == 'addr':
                self.handle_addr(line)
            elif msgtype == 'question':
                self.handle_question(line)
            elif msgtype == 'response':
                self.handle_response(line)

    def send_pong(self):
        pong = json.dumps({'msgtype': 'pong'})
        self.write(pong)

    def handle_ping(self):
        self.send_pong()

    # The first message that gets sent
    def send_hello(self):
        hello = json.dumps({'nodeid': self.nodeid, 'msgtype': 'hello'})
        self.write(hello)
        self.state = "SENTHELLO"

    # Method that takes question requests and adds them to a queue
    def handle_question(self, question):
        json1 = json.loads(question)
        self.factory.questions[self.factory.questionID] = json1["question"]
        print("Got this quesiton: ", self.factory.questions[self.factory.questionID])
        self.factory.questionID = self.factory.questionID + 1

    # Method that sends out the questions in the queue to the nodes
    def send_question(self):
        questions = self.factory.questions
        print(questions)
        if (questions) and (self.lastQuestion != self.factory.questionID):
            question = [(n, questions[n][0])
                        for n in itertools.islice(questions, self.lastQuestion, None)]

            message = json.dumps({'msgtype': 'question', 'question': question})
            print(" [>] Sending: ", question, " to ", self.remote_nodeid, self.remote_ip,)
            self.write(message)
            self.lastQuestion = self.factory.questionID

        else:
            _print(" [ ] No questions to send")

    def handle_response(self, response):
        responses = json.loads(response)
        for answer in responses["response"]:
            print(" [<] Answer from ", self.remote_nodeid, self.remote_ip, "is ", answer)

    # Handle the addresses that get sent by other nodes, and contact them
    def handle_addr(self, addr):
        json1 = json.loads(addr)
        for node in json1["nodes"]:
            if node[0] == self.nodeid:
                continue
            if node[2] == "SPEAKER":
                continue
            if node[0] in self.factory.peers:
                continue
            host, port = node[1].split(":")
            point = TCP4ClientEndpoint(reactor, host, int(port))
            d = connectProtocol(point, COProtocol(self.factory, "HELLO", "SPEAKER"))
            d.addCallback(gotProtocol)

    # Handle the first message that gets sent
    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_nodeid = hello["nodeid"]
        print("Got hello from: " , self.remote_nodeid, self.remote_ip)

        if self.remote_nodeid == self.nodeid:
            print (" [!] Connected to myself.")
            self.transport.loseConnection()
        else:
            if self.state == "HELLO" :
                self.add_peer("SPEAKER")
            elif self.state == "SENTHELLO":
                self.add_peer("LISTENER")

            self.send_hello()

            _print(" [ ] Adding ", self.remote_nodeid, " to question list")
            self.lc_question.start(QUESTION_INTERVAL, now=False)

    def add_peer(self, kind):
        entry = (self.remote_ip, kind)
        self.factory.peers[self.remote_nodeid] = entry

def gotProtocol(p):
    """The callback to start the protocol exchange. We let connecting
    nodes start the hello handshake"""
    p.send_hello()