import testFrame
import ml
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.utils import check_random_state
import random

def data():
    imgs = {"data": [], "labels": []}

    X, y = fetch_openml('mnist_784', version=1, return_X_y=True)
    train_samples = 50000

    random_state = check_random_state(0)
    permutation = random_state.permutation(X.shape[0])
    X = X[permutation]
    y = y[permutation]
    X = X.reshape((X.shape[0], -1))

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_samples, test_size=10000)
    imgs["data"].append(X_train)
    imgs["labels"].append(y_train)

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
        self.ml = ml.mlsgd(imgs, "0")

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