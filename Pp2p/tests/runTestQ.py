import socket
import sys
import json

HOST, PORT = "localhost", 5005

m0 =({'msgtype': 'question', 'question': ["This question!", "This question too!"]})
jsonObj0 = json.dumps(m0)

data0 = (jsonObj0.encode('utf-8'))

m1 =({'msgtype': 'question', 'question': ["This question!", "This question too!"]})
jsonObj1 = json.dumps(m1)

data1  = (jsonObj1.encode('utf-8'))

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data0)

    sleep(45)

    sock.sendall(data1)

finally:
    sock.close()

