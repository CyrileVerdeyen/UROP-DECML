## Code addapted from https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html
## Author: Cyrile Verdeyen

import json
from time import time

from twisted.internet import reactor
from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint,
                                        connectProtocol)
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall

from crypto import generate_nodeid

## The factory class houses all the different protocols that each node has, as well as any other constant data. 
class PPFactory(Factory):
    def __init__(self):
        pass

    def startFactory(self):
        self.peers = {}
        self.nodeid = generate_nodeid()
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return PPProtocol(self)

## The PPProtocol is where the communication happens between each of the nodes. This handles the sending, recieving and handling of the data.
class PPProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.state = "HELLO"
        self.remote_nodeid = None
        self.nodeid = self.factory.nodeid
        self.lc_ping = LoopingCall(self.send_ping)
        self.lastping = None

    # This method gets called everytime a connection gets made to a node.
    def connectionMade(self):
        remote_ip = self.transport.getPeer()
        host_ip = self.transport.getHost()  
        self.remote_ip = remote_ip.host + ":" + str(remote_ip.port)
        self.host_ip = host_ip.host + ":" + str(host_ip.port)
        self.factory.numProtocols = self.factory.numProtocols + 1
        print ("Connection from", self.transport.getPeer(), " Number of connections: ", self.factory.numProtocols)

    # This gets called everytime a node dissconects.
    def connectionLost(self, reason):
        if self.remote_nodeid in self.factory.peers:
            self.factory.peers.pop(self.remote_nodeid)
            try: self.lc_ping.stop()
            except AssertionError: pass
        self.factory.numProtocols = self.factory.numProtocols - 1
        print ("A Node dissconected. Connections left ", self.factory.numProtocols)

    # dataRecieved gets called everytime new bytes arrive at the port that is being listened to.
    def dataReceived(self, data):
        print("Recieved data")
        for line in (data.splitlines()):
            line = line.strip()
            msgtype = json.loads(line)['msgtype']
            if self.state == "HELLO" or msgtype == "hello":
                self.handle_hello(line)
                self.state = "READY"
            elif msgtype == "ping":
                self.handle_ping()
            elif msgtype == "pong":
                self.handle_pong()

    # The first message that gets sent
    def send_hello(self):
        hello = json.dumps({'nodeid': self.nodeid, 'msgtype': 'hello'})
        print("Sending Hello")
        self.transport.write(hello.encode('utf-8') + "\n")

    # Ping pongs are used to verify the excistance of nodes, and making sure that they have not disconected.
    def send_ping(self):
        ping = json.dumps({'msgtype': 'ping'})
        print ("Pinging", self.remote_nodeid)
        self.transport.write((ping + "\n").encode('utf-8'))

    def send_pong(self):
        pong = json.dumps({'msgtype': 'pong'})
        self.transport.write((pong + "\n").encode('utf-8'))

    def handle_ping(self):  
        self.send_pong()

    def handle_pong(self):
        print ("Got pong from", self.remote_nodeid)
        ###Update the timestamp
        self.lastping = time()

    # Send the addresses to other nodes and own node
    def send_addr(self, mine=False):
        now = time()
        if mine:
            peers = [self.host_ip]
        '''else:
            peers = [(peer.remote_ip, peer.remote_nodeid)
                     for peer in self.factory.peers
                     if peer.lastping > now-240]
            self.transport.write(peers + "\n")'''

    # Handle the addresses that get sent by other nodes, and contact them
    def handle_addr(self, addr):
        json1 = json.loads(addr)
        for remote_ip, remote_nodeid in json1["peers"]:
            if remote_nodeid not in self.factory.peers:
                host, port = remote_ip.split(":")
                point = TCP4ClientEndpoint(reactor, host, int(port))
                d = connectProtocol(point, PPProtocol(2))
                d.addCallback(gotProtocol)

    def handle_getaddr(self, getaddr):
        self.send_addr()

    #Handle the first message that gets sent
    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_nodeid = hello["nodeid"]
        print("Got hello from: " , self.remote_nodeid)
        if self.remote_nodeid == self.nodeid:
            print ("Connected to myself.")
            self.transport.loseConnection()
        else:
            print ("Pinging")
            self.factory.peers[self.remote_nodeid] = self
            self.lc_ping.start(30)
            ###inform our new peer about us
            self.send_addr(mine=True)
            ###and ask them for more peers
            self.send_addr(mine=False)

def gotProtocol(p):
    """The callback to start the protocol exchange. We let connecting
    nodes start the hello handshake""" 
    p.send_hello()