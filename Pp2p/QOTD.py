from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away\r\n".encode('utf-8')) 
        self.transport.loseConnection()
    
class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()

endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(QOTDFactory())
reactor.run()