import testFrame
import ml
import random
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.utils import check_random_state
import socket

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

class CO():
    def __init__(self, data=False):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.DEFAULT_PORT = 5005
        self.BOOTSRAP_NODES = []
        self.data = data

    def run(self):
        server = testFrame.testCO(self.DEFAULT_PORT, self.BOOTSRAP_NODES, Host=self.ip, data=self.data)
        server.server()
        server.client()

class node():
    def __init__(self):

        self.ip = socket.gethostbyname(socket.gethostname())

        imgs = {"data": [], "labels": []}

        X, y = fetch_openml('mnist_784', version=1, return_X_y=True)
        train_samples = 25000

        seed = random.randint(0,100)
        random_state = check_random_state(seed)
        permutation = random_state.permutation(X.shape[0])
        X = X[permutation]
        y = y[permutation]
        X = X.reshape((X.shape[0], -1))

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_samples, test_size=10000)
        imgs["data"].append(X_train)
        imgs["labels"].append(y_train)

        self.DEFAULT_PORT = 5006
        self.BOOTSRAP_NODES = ["10.221.31.232:5005"]

        self.ml = ml.mlsvm(imgs, "0")

    def run(self):
        server = testFrame.testPP(self.DEFAULT_PORT, self.BOOTSRAP_NODES, self.ml, Host=self.ip)
        server.server()
        server.client()