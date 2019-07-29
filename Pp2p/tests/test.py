import testFrame
import ml
import random

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

class CO():
    def __init__(self):
        self.DEFAULT_PORT = 5005
        self.BOOTSRAP_NODES = []

    def run(self):
        server = testFrame.testCO(self.DEFAULT_PORT, self.BOOTSRAP_NODES)
        server.server()
        server.client()

class node():
    def __init__(self):
        batch = random.randint(1, 5)

        self.DEFAULT_PORT = 5006
        self.BOOTSRAP_NODES = ["localhost:5005"]

        imgs = unpickle("./cifar-10-batches-py/data_batch_" + str(batch))
        self.ml = ml.mlsvm(imgs, "0")

    def run(self):
        server = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml)
        server.server()
        server.client()