# Sample Decision Tree Classifier
from sklearn import datasets
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm
import joblib
import os.path
from time import time
from datetime import datetime

def _print(*args):
    # double, make common module
    time = datetime.now().time().isoformat()[:8]
    print (time)
    print ("".join(map(str, args)))

class mlsvm():

    def __init__(self, imgs, ID):

        if os.path.exists('saved_model' + str(ID) + '.pkl'):
            self.clf = joblib.load('saved_model' + str(ID) + '.pkl')
        else:
            self.imgs = imgs
            X = self.imgs["data"][0]
            Y = self.imgs["labels"][0]
            _print("Running the ML")
            self.clf = svm.SVC(gamma='scale', decision_function_shape='ovo', probability=True)
            self.clf.fit(X, Y)
            _print("Finished training ML")
            joblib.dump(self.clf, 'saved_model' + str(ID) + '.pkl')

    def classify(self, img):
        self.img = img
        predict = self.clf.predict_proba(self.img)[0]
        prediction = self.clf.predict(self.img)
        return ([prediction.tolist(), predict[(int(prediction))].tolist()])

class mlnn():

    def __init__(self, imgs, ID):

        if os.path.exists('saved_model' + str(ID) + '.pkl'):
            self.clf = joblib.load('saved_model' + str(ID) + '.pkl')
        else:
            self.imgs = imgs
            X = self.imgs["data"][0]
            Y = self.imgs["labels"][0]
            _print("Running the ML")
            self.clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(100, 20), random_state=1, early_stopping=True)
            self.clf.fit(X, Y)
            _print("Finihsed running the ML")
            joblib.dump(self.clf, 'saved_model' + str(ID) + '.pkl')

    def classify(self, img):
        self.img = img
        predict = self.clf.predict_proba(self.img)[0]
        prediction = self.clf.predict(self.img)
        return ([prediction.tolist(), predict[(int(prediction))].tolist()])

class mlsgd():

    def __init__(self, imgs, ID):

        if os.path.exists('saved_model' + str(ID) + '.pkl'):
            self.clf = joblib.load('saved_model' + str(ID) + '.pkl')
        else:
            self.imgs = imgs
            X = self.imgs["data"][0]
            Y = self.imgs["labels"][0]
            _print("Running the ML")
            self.clf = SGDClassifier(loss="modified_huber", penalty="l2", max_iter=400, early_stopping=False, shuffle=True, learning_rate='optimal')
            self.clf.fit(X, Y)
            _print("Finished running the ML")
            joblib.dump(self.clf, 'saved_model' + str(ID) + '.pkl')

    def classify(self, img):
        self.img = img
        predict = self.clf.predict_proba(self.img)[0]
        prediction = self.clf.predict(self.img)
        return ([prediction.tolist(), predict[(int(prediction))].tolist()])

    def update(self, img):
        self.img = img
        X = self.img["data"][0]
        Y = self.img["labels"][0]
        self.clf.partial_fit(X, Y)

class mlrf():

    def __init__(self, imgs, ID):

        if os.path.exists('saved_model' + str(ID) + '.pkl'):
            self.clf = joblib.load('saved_model' + str(ID) + '.pkl')
        else:
            self.imgs = imgs
            X = self.imgs["data"][0]
            Y = self.imgs["labels"][0]
            _print("Running the ML")
            self.clf = RandomForestClassifier(n_estimators=200, max_depth=2, max_features=55, random_state=0)
            self.clf.fit(X, Y)
            _print("Finished running the ML")
            joblib.dump(self.clf, 'saved_model' + str(ID) + '.pkl')
            print(self.clf)

    def classify(self, img):
        self.img = img
        predict = self.clf.predict_proba(self.img)[0]
        prediction = self.clf.predict(self.img)
        return ([prediction.tolist(), predict[(int(prediction))].tolist()])