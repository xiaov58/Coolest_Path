
# ccc_server.py
import socket
import select
import threading
import meta_data
import cPickle
from control_msg import *

class ccc_server(threading.Thread):
    def __init__(self, threadname,  options, crn_manager):
        threading.Thread.__init__(self, name = threadname)
        self.options = options
        self.crn_manager = crn_manager
        self.port = meta_data.server_port;
        self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.srvsock.bind( ("", meta_data.server_port) )
        self.srvsock.listen( meta_data.max_client )
        self.descriptors = [self.srvsock]
        print 'Control Server started on node %d' % (int(self.options.id))
        
    def run(self):
     while 1:
        # Await an event on a readable socket descriptor
        (sread, swrite, sexc) = select.select( self.descriptors, [], [])
    
        # Iterate through the tagged read descriptors
        for sock in sread:
    
          # Received a connect to the server (listening) socket
          if sock == self.srvsock:
            self.accept_new_connection()
          else:
            # Received something on a client socket
            str = sock.recv(meta_data.sock_buffer_size)
            if str == "":
                host,port = sock.getpeername()
                str = 'Client closed %s:%s' % (host, port)
                sock.close
                self.descriptors.remove(sock)
            else:
                ctrl_msg = cPickle.loads(str)
                print "control_msg: %d" % ctrl_msg.type
                
    
    def accept_new_connection(self):
      newsock, (remhost, remport) = self.srvsock.accept()
      self.descriptors.append( newsock )
    
      newsock.send("Connected to ccc_server on node %d" % (int(self.options.id)))
      str = "Client joined %s:%s" % (remhost, remport)
      print str
