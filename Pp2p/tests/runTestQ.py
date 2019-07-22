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
question = imgs1[b"data"][1].tolist()
answer = imgs1[b"labels"][1]
print(answer, nameImg(answer))

HOST, PORT = "localhost", 5005

m0 =({'msgtype': 'question', 'question': [question]})
jsonObj0 = json.dumps(m0)

data0 = (jsonObj0.encode('utf-8'))

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data0)

    time.sleep(20)

    while (True):
        answer = sock.recv(512)
        message = json.loads(answer)
        for response in message["response"]:
            print("For quesiton: ", response[0], " the answer is: ", response[1], " which is a: ", nameImg(response[1]))


finally:
    sock.close()
