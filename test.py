import socket
import sys
import json


def add():

    host, port = "localhost", 6002
    data = " ".join(sys.argv[1:])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(dict(
            CMD='ADD',
            TABLE='RunTime',
            PARA=dict(id='3', module='WEB')
        )))

        # Receive data from the server and shut down
        received = sock.recv(1024)
        print "Sent:     {}".format(data)
        print "Received: {}".format(received)
    finally:
        sock.close()


def search():

    host, port = "localhost", 6002
    data = " ".join(sys.argv[1:])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        sock.connect((host, port))
        sock.sendall(json.dumps(dict(
            CMD='SEARCH',
            TABLE='RunTime',
            PARA=dict()
        )))

        received = sock.recv(1024)
        print "Sent:     {}".format(data)
        print "Received: {}".format(received)

    finally:
        sock.close()

add()
search()
