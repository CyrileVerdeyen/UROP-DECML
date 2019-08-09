import testFrame
import ml
from sklearn.externals import joblib
import random

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def data():
    imgs = {b"data": [], b"labels": []}

    for i in (range (1,6)):
        img = unpickle("./cifar-10-batches-py/data_batch_" + str(i))
        for j in range(10000):
            imgs[b"data"].append(img[b"data"][(j)])
            imgs[b"labels"].append(img[b"labels"][(j)])

    return imgs

class CO():
    def __init__(self):
        self.DEFAULT_PORT = 5005
        self.BOOTSRAP_NODES = []

    def run(self):
        server = testFrame.testCO(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server.server()
        server.client()

class node0():
    def __init__(self):
        self.DEFAULT_PORT = 5008
        self.BOOTSRAP_NODES = ["localhost:5005"]

        imgs = data()
        self.ml = ml.mlsvm(imgs, "0")

    def run(self):
        server = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server.server()
        server.client()

class node1():
    def __init__(self):
        self.DEFAULT_PORT = 5009
        self.BOOTSRAP_NODES = ["localhost:5005",
                                "localhost:5008"]

        imgs = data()
        self.ml = ml.mlsvm(imgs, "1")

    def run(self):
        server1 = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server1.server()
        server1.client()

class node2():
    def __init__(self):
        self.DEFAULT_PORT = 5010
        self.BOOTSRAP_NODES = ["localhost:5005",
                                "localhost:5008",
                                "localhost:5009"]

        imgs = data()
        self.ml = ml.mlsvm(imgs, "2")

    def run(self):
        server2 = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server2.server()
        server2.client()

class node3():
    def __init__(self):
        self.DEFAULT_PORT = 5011
        self.BOOTSRAP_NODES = ["localhost:5005",
                                "localhost:5008",
                                "localhost:5009"]

        imgs = data()
        self.ml = ml.mlsvm(imgs, "3")


    def run(self):
        server3 = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server3.server()
        server3.client()

class node4():
    def __init__(self):
        self.DEFAULT_PORT = 5012
        self.BOOTSRAP_NODES = ["localhost:5005",
                                "localhost:5011"]

        imgs = data()
        self.ml = ml.mlsvm(imgs, "4")

    def run(self):
        server4 = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server4.server()
        server4.client()

class node5():
    def __init__(self):
        self.DEFAULT_PORT = 5013
        self.BOOTSRAP_NODES = ["localhost:5005",
                                "localhost:5012"]

    def run(self):
        server5 = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server5.server()
        server5.client()