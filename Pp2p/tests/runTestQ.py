import socket
import sys
import json
import time


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def nameImg(ID):
    images = unpickle("./cifar-10-python/cifar-10-batches-py/batches.meta")
    return images[b"label_names"][ID]


imgs1 = unpickle("./cifar-10-python/cifar-10-batches-py/test_batch")
question0 = imgs1[b"data"][372].tolist()
answer0 = imgs1[b"labels"][372]
print("The expected answer for 0 is: ", answer0, " Which is a: ", nameImg(answer0))

question1 = imgs1[b"data"][486].tolist()
answer1 = imgs1[b"labels"][486]
print("The expected answer for 1 is: ", answer1, " Which is a: ", nameImg(answer1))

question2 = imgs1[b"data"][7322].tolist()
answer2 = imgs1[b"labels"][7322]
print("The expected answer for 2 is: ", answer2, " Which is a: ", nameImg(answer2))

HOST, PORT = "localhost", 5005

m0 =({'msgtype': 'question', 'question': [question0]})
jsonObj0 = json.dumps(m0)

data0 = (jsonObj0.encode('utf-8'))

m1 =({'msgtype': 'question', 'question': [question1]})
jsonObj1 = json.dumps(m1)

data1 = (jsonObj1.encode('utf-8'))

m2 =({'msgtype': 'question', 'question': [question2]})
jsonObj2 = json.dumps(m2)

data2 = (jsonObj2.encode('utf-8'))


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data0)

    time.sleep(20)

    sock.sendall(data1)

    time.sleep(20)

    sock.sendall(data2)

    while (True):
        answer = sock.recv(512)
        message = json.loads(answer)
        for response in message["response"]:
            print("For quesiton: ", response[0], " the answer is: ", response[1], " which is a: ", nameImg(response[1]))


finally:
    sock.close()
