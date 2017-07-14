import zmq
import random
import sys
import time
import json

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

msg_json = {
        "user_text": "Hi I lost my card",
        "user_name": "Avinash"
            }

while True:
    socket.send_json(msg_json)
    msg = socket.recv_json()
    print(msg, "Received from client")
    time.sleep(1)