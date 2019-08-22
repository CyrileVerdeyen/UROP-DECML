import socket
import sys
import json
import time
import random
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.utils import check_random_state
from sklearn.metrics import accuracy_score
import os


imgs = {"data": [], "labels": []}

X, y = fetch_openml('mnist_784', version=1, return_X_y=True)
train_samples = 50000

random_state = check_random_state(0)
permutation = random_state.permutation(X.shape[0])
X = X[permutation]
y = y[permutation]
X = X.reshape((X.shape[0], -1))

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_samples, test_size=1000)
imgs["data"].append(X_test)
imgs["labels"].append(y_test)

true_answers = []
answers = []

def createQuestion(number):

    question0 = imgs["data"][0][number].tolist()
    answer0 = imgs["labels"][0][number]
    print("The expected answer is: ", answer0)
    true_answers.append(answer0)

    m0 =({'msgtype': 'question', 'question': [question0]})
    jsonObj0 = json.dumps(m0)

    data0 = (jsonObj0.encode('utf-8'))

    return ((data0+b"\r\n"),answer0)

HOST, PORT = "10.221.31.232", 5005
quesitonsSent = 0
correctAnswers = 0

if (os.path.exists("tests.txt")):
    os.remove("tests.txt")

log = open("tests.txt", "w+")

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    num = 1
    QA = createQuestion(num)
    sock.sendall(QA[0])
    quesitonsSent += 1

    time.sleep(5)

    while (num < 999):
        answer = sock.recv(512)
        message = json.loads(answer)
        for response in message["response"]:
            message = ("For quesiton: " + str(response[0]) + " the answer is: " + str(response[1]))
            print(message)
            if int(response[1]) == int(QA[1]):
                correctAnswers += 1
            score = ("Correct Responses: " + str(correctAnswers) + "/" + str(quesitonsSent))
            print(score)
            log.write(score + "\r\n")
            answers.append(int(response[1]))

        num += 1
        QA = createQuestion(num)
        sock.sendall(QA[0])
        quesitonsSent += 1

        time.sleep(15)
        answers.append(int(response[1]))

finally:
    sock.close()

accuracy = accuracy_score(true_answers, answers)
print("Accuracy is: ", accuracy)