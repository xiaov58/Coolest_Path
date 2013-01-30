
# crn_manager.py: control ccc_server and main schedule loop

# from system
from __future__ import division
import sys
import socket
import time
import threading
import cPickle


# from current dir
import meta_data
from ccc_server import ccc_server
from destination import destination
from source import source
from router import router
from control_msg import *


class crn_manager: 
    def __init__(self, options):
        self.options = options
        self.id = int(options.id)
        self.neighbor_socks_table = {}
        
        
    def establish_ccc(self):
        # start ccc_server, receive incoming control msg only
        ccc_server_ = ccc_server("ccc_server", self)
        ccc_server_.setDaemon(True)
        ccc_server_.start()
        
        # wait a while for setting up servers on all other nodes
        time.sleep(meta_data.ccc_server_setup_time)
        
        # establish connection to server, use dict to store neighbor sock info
        # key is the node id, value is the sock descriptor
        for i in meta_data.neighbour_table[self.id]:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( (meta_data.ip_table[i], meta_data.server_port) )
            print sock.recv( meta_data.sock_buffer_size )
            self.neighbor_socks_table[i] = sock
            
            
            