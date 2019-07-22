# Sample Decision Tree Classifier
from sklearn import datasets
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.externals import joblib
import os.path

class ml():

    def __init__(self, imgs, ID):

        if os.path.exists('saved_model' + str(ID) + '.pkl'):
            self.clf = joblib.load('saved_model' + str(ID) + '.pkl')
        else:
            self.imgs = imgs
            X = self.imgs[b"data"]
            Y = self.imgs[b"labels"]
            self.clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
            self.clf.fit(X, Y)
            joblib.dump(self.clf, 'saved_model' + str(ID) + '.pkl')

        print(self.clf)

    def classify(self, img):
        self.img = img
        return self.clf.predict(self.img).tolist()