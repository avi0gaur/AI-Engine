import sys
import zmq
import time
from chat_bot import CrmnextChatBot

"""
The Python code below will create an echo server that listens on port 5000 with a REP socket. 
It will then loop an alternation of performing .recv() for incoming requests and then .send() a reply to them.
"""



bot = CrmnextChatBot()
port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    msg = socket.recv_json()
    res = bot.run_bot(msg)
    socket.send_json(res)
    time.sleep(1)