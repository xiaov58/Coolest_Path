import socket
import select

class CCC_Server:
    def __init__(self, port):
        self.port = port;
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_sock.bind(("",port))
        self.server_sock.listen(3)
        self.descriptors = [self.server_sock]
        print "CCC_Server started on %s" % port

    def run(self):
        while 1:
            # Wait an event on a readable socket descriptor
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])

            # Iterate through the tagged read descriptor
            for sock in sread:

                # Received a connection to the server (listening) socket
                if sock == self.server_sock:
                    self.accept_new_connection()
                #else:
                    # Received something on a client socket
                    #msg = sock.recv(100)
                    #peer_ip, peer_port = sock.getpeername()
                    #print "[%s;%s]:%s" % (peer_ip, peer_port, str)

    def accept_new_connection(self):
        newsock, (peer_host, peer_port) = self.server_sock.accept()
        self.descriptors.append(newsock)
        newsock.send("Connected to server")
        msg = "Client joined [%s;%s]" % (peer_host, peer_port)

ccc_server = CCC_Server(11012)
ccc_server.run()
