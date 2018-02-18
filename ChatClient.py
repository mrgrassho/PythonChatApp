#! bin/env python3

"""Client for Simple Chat Server."""

import socket
import threading
import blessings
import os


class ChatClient:
    """Chat client class."""

    def __init__(self, ip, port):
        """Create a connection on a given address."""
        self.port = port
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.connect((ip, port))
        self.thread_receive = threading.Thread(target=self.receive_msg)
        self.thread_send = threading.Thread(target=self.send_msg)
        self.t = blessings.Terminal()
        self.th = self.t.height
        self.tw = self.t.width
        self.k = 1
        self.flag = True
        os.system('clear')

    def receive_msg(self):
        """Receive messages from the outside.

        TODO:Add a check control to the buffer length.
        """
        while True:
            try:
                msg = self.srvsock.recv(100)
                with self.t.location(0, self.k):
                    print(msg.decode())
                self.k = self.k + 1
            except BaseException as e:
                print('Server Error! Connection shut down.')
                raise e

    def send_msg(self):
        """Send messages to the server."""
        while True:
            msg = input()
            # Added to show logs clean at the first time
            # a conncetion send a message.
            if(self.flag):
                self.k = self.k + 1
                self.flag = False
            self.srvsock.send(bytes(msg, encoding='utf-8'))

    def run(self):
        """Run the client.

        It's important to initialize a thread with one of the methods(receive
        or send) in order to receive/send messages both at the same time.
        """
        # self.thread_send.start()
        self.thread_receive.start()
        # self.receive_msg()
        self.send_msg()


c = ChatClient('localhost', 2626)
c.run()
