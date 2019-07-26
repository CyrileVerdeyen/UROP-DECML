import ml
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

data = unpickle("tests/cifar-10-batches-py/data_batch_1")
data.update(unpickle("tests/cifar-10-batches-py/data_batch_2"))
data.update(unpickle("tests/cifar-10-batches-py/data_batch_3"))
data.update(unpickle("tests/cifar-10-batches-py/data_batch_4"))
data.update(unpickle("tests/cifar-10-batches-py/data_batch_5"))

ml = ml.mlsvm(data, "0")

test = unpickle("tests/cifar-10-batches-py/test_batch")
test_true = []
answers = []

for i in (range (1000)):
    question = test[b"data"][(i+1)].reshape(1, -1)
    answer = ml.classify(question)
    answers.append(answer[0])
    test_true.append(test[b"labels"][i+1])

accuracy = accuracy_score(test_true, answers)
print("Accuracy is: ", accuracy)