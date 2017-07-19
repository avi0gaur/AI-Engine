import zmq
import time
from zm_pub import PubUser

__author__ = 'avi0gaur'

"""
The Python code below will create an echo server that listens on port 5556 with a SUB socket. 
It will then loop an alternation of performing .recv_json() for incoming requests and then .send_json() a reply to them.
"""

'''
Port and IP to bind.
Ensure the port is available 
'''

port_sub = "5556"
sub_ip = "192.168.0.56"
pb = PubUser()

def init_res():
    """
    Method initialize subscriber to get user data with chat response
    :return:
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://" + sub_ip + ":" + port_sub)
    socket.setsockopt_string(zmq.SUBSCRIBE,'')

    while True:
        msg = socket.recv_json()
        print(str(msg))
        pb.pub(msg)
        time.sleep(1)


if __name__ == '__main__':
    """
    Init subscriber to bind with the socket 
    """
    init_res()
