import testFrame

class node0():
    def __init__(self):
        self.DEFAULT_PORT = 5008
        self.BOOTSRAP_NODES = []

    def run(self):
        server = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server.server()
        server.client()

class node1():
    def __init__(self):
        self.DEFAULT_PORT = 5009
        self.BOOTSRAP_NODES = ["localhost:5008"]

    def run(self):
        server1 = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server1.server()
        server1.client()

class node2():
    def __init__(self):
        self.DEFAULT_PORT = 5010
        self.BOOTSRAP_NODES = ["localhost:5008",
                                "localhost:5009"]

    def run(self):
        server2 = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server2.server()
        server2.client()

class node3():
    def __init__(self):
        self.DEFAULT_PORT = 5011
        self.BOOTSRAP_NODES = ["localhost:5008",
                                "localhost:5009"]

    def run(self):
        server3 = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server3.server()
        server3.client()

class node4():
    def __init__(self):
        self.DEFAULT_PORT = 5012
        self.BOOTSRAP_NODES = ["localhost:5011"]

    def run(self):
        server4 = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server4.server()
        server4.client()

class node5():
    def __init__(self):
        self.DEFAULT_PORT = 5013
        self.BOOTSRAP_NODES = ["localhost:5012"]

    def run(self):
        server5 = testFrame.test(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server5.server()
        server5.client()