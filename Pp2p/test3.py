import argparse
from datetime import datetime
from threading import Thread

from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint) 
from twisted.internet import reactor
from twisted.internet.error import CannotListenError
from twisted.internet.endpoints import connectProtocol

from network import (PPFactory, PPProtocol, gotProtocol)

def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))


# Move this and network.BOOTSTRAP_NODES somewhere mode sensible
DEFAULT_PORT = 5011

parser = argparse.ArgumentParser(description="server")
parser.add_argument('--port', type=int, default=DEFAULT_PORT)
parser.add_argument('--listen', default="localhost")
parser.add_argument('--bootstrap', action="append", default=[])

args = parser.parse_args()

try:
    endpoint = TCP4ServerEndpoint(reactor, args.port, interface=args.listen)
    _print(" [ ] LISTEN:", args.listen, ":", args.port)
    ppfactory = PPFactory()
    endpoint.listen(ppfactory)
except CannotListenError:
    _print("[!] Address in use")
    raise SystemExit

BOOTSTRAP_NODES = ["localhost:5008",
                   "localhost:5009"]

_print(" [ ] Trying to connect to host : localhost:5008")


for bootstrap in BOOTSTRAP_NODES + [a+":"+str(DEFAULT_PORT) for a in args.bootstrap]:

    _print("     [*] ", bootstrap)
    host, port = bootstrap.split(":")
    point = TCP4ClientEndpoint(reactor, host, int(port))
    d = connectProtocol(point, PPProtocol(ppfactory))
    d.addCallback(gotProtocol)
reactor.run()

#Thread(target=reactor.run, args=(False,)).start()
