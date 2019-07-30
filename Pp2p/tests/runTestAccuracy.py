import socket
import sys
import json
import time
import random
from sklearn.metrics import accuracy_score


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def nameImg(ID):
    images = unpickle("./cifar-10-batches-py/batches.meta")
    return images[b"label_names"][ID]

imgs1 = unpickle("./cifar-10-batches-py/test_batch")

true_answers = []
answers = []

def createQuestion(number):

    question0 = imgs1[b"data"][number].tolist()
    answer0 = imgs1[b"labels"][number]
    print("The expected answer is: ", answer0, " Which is a: ", nameImg(answer0))
    true_answers.append(answer0)

    m0 =({'msgtype': 'question', 'question': [question0]})
    jsonObj0 = json.dumps(m0)

    data0 = (jsonObj0.encode('utf-8'))

    return (data0,answer0)

HOST, PORT = "localhost", 5005
quesitonsSent = 0
correctAnswers = 0

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

    while (num < 997):
        answer = sock.recv(512)
        message = json.loads(answer)
        for response in message["response"]:
            print("For quesiton: ", response[0], " the answer is: ", response[1], " which is a: ", nameImg(int(response[1])))
            if int(response[1]) == QA[1]:
                correctAnswers += 1
            print("Correct Responses: ", correctAnswers, "/", quesitonsSent)
            answers.append(int(response[1]))

        num += 1
        QA = createQuestion(num)
        sock.sendall(QA[0])
        quesitonsSent += 1

        time.sleep(5)


finally:
    sock.close()

accuracy = accuracy_score(true_answers, answers)
print("Accuracy is: ", accuracy)