import socket
import sys
import json

HOST, PORT = "localhost", 5005

m =({'msgtype': 'question', 'question': ["This question!", "This question too!"]})
jsonObj = json.dumps(m)


data = (jsonObj.encode('utf-8'))

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data)

finally:
    sock.close()

print( "Sent:     {}".format(data))
