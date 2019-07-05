import argparse
from datetime import datetime
from threading import Thread

from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint) 
from twisted.internet import reactor
from twisted.internet.error import CannotListenError
from twisted.internet.endpoints import connectProtocol

import sys
sys.path.append("..")
from network import (PPFactory, PPProtocol, gotProtocol)

def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))

class test():

    def __init__(self, Port, BootstrapNodes=[]):

        self.BOOTSTRAP_NODES = BootstrapNodes
        self.DEFAULT_PORT = Port

        parser = argparse.ArgumentParser(description="server")
        parser.add_argument('--port', type=int, default=self.DEFAULT_PORT)
        parser.add_argument('--listen', default="localhost")
        parser.add_argument('--bootstrap', action="append", default=[])

        self.args = parser.parse_args()

    def server(self):
        try:
            endpoint = TCP4ServerEndpoint(reactor, self.args.port, interface=self.args.listen)
            _print(" [ ] LISTEN:", self.args.listen, ":", self.args.port)
            self.ppfactory = PPFactory()
            endpoint.listen(self.ppfactory)
        except CannotListenError:
            _print("[!] Address in use")
            raise SystemExit

    def client(self):
        
        _print(" [ ] Trying to connect to host : localhost:", self.DEFAULT_PORT)

        for bootstrap in self.BOOTSTRAP_NODES + [a+":"+str(self.DEFAULT_PORT) for a in self.args.bootstrap]:

            _print("     [*] ", bootstrap)
            host, port = bootstrap.split(":")
            point = TCP4ClientEndpoint(reactor, host, int(port))
            d = connectProtocol(point, PPProtocol(self.ppfactory))
            d.addCallback(gotProtocol)
        reactor.run()

        #Thread(target=reactor.run, args=(False,)).start()
