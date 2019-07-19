# Sample Decision Tree Classifier
from sklearn import datasets
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm

class ml():

    def __init__(self, imgs):
        self.imgs = imgs
        X = self.imgs[b"data"]
        Y = self.imgs[b"labels"]
        self.clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
        self.clf.fit(X, Y)

        print(self.clf)

    def classify(self, img):
        self.img = img
        return self.clf.predict(self.img)