#! bin/env python3

"""Chat Server for Chat App."""

import socket
import select


class ChatServer:
    """Class for ChatServer."""

    def __init__(self, port, verbose=False):
        """Create a chat server on a given port."""
        self.port = port
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind(('localhost', port))
        self.srvsock.listen(5)
        self.descriptors = [self.srvsock]
        self.verbose = verbose
        if (self.verbose):
            print('ChatServer started on port %s' % port)

    def run(self):
        """Run the server."""
        while True:
            # Await an event on a readable socket descriptor
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])
            # Iterate through the tagged read descriptors
            for sock in sread:
                # Received a connect to the server (listening) socket
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    # Received something on a client socket
                    str = sock.recv(100).decode()
                    # Check to see if the peer socket closed
                    if str == '':
                        host, port = sock.getpeername()
                        str = 'Client left %s:%s\r' % (host, port)
                        self.broadcast_string(str)
                        sock.close
                        self.descriptors.remove(sock)
                    else:
                        host, port = sock.getpeername()
                        newstr = '[%s:%s] %s' % (host, port, str)
                        self.broadcast_string(newstr)

    def broadcast_string(self, msg):
        """Send data to all the connected sockets."""
        for sock in self.descriptors:
            if sock != self.srvsock:
                sock.send(bytes(msg))
        if (self.verbose):
            print(msg)

    def accept_new_connection(self):
        """Acept new connections to the server."""
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        msg = "You're connected to the ChatServer App.\r\n"
        newsock.send(bytes(msg))
        str = 'Client joined %s:%s\r' % (remhost, remport)
        self.broadcast_string(str)


myServer = ChatServer(2626, verbose=True)
myServer.run()
