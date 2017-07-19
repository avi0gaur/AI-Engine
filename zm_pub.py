import sys
import zmq
import time
import random
from chat_bot import CrmnextChatBot

__author__ = 'avi0gaur'

class PubUser:

    bot = CrmnextChatBot()

    def __init__(self):
        """
        Configuration for publisher to send bot response to .net layer
        """
        port = "5557"
        ip = "192.168.0.40"
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect("tcp://" + ip + ":" + port)

    def pub(self, res):
        """
        This method is associated with calling bot logic and sending the response to .net layer
        :param res:
        :return:
        """
        conv = self.bot.run_bot(res)
        print(conv)
        self.socket.send_json(conv)