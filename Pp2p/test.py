from twisted.internet.endpoints import (TCP4ClientEndpoint, TCP4ServerEndpoint,
                                        connectProtocol)
from twisted.internet import reactor

from network import (PPFactory, PPProtocol, gotProtocol)

endpoint = TCP4ServerEndpoint(reactor, 5999)
endpoint.listen(PPFactory())

endpoint = TCP4ServerEndpoint(reactor, 5998)
endpoint.listen(PPFactory())

point = TCP4ClientEndpoint(reactor, "localhost", 599)
myfactory = PPFactory()
d = connectProtocol(point, PPProtocol(myfactory))
d.addCallback(gotProtocol)
