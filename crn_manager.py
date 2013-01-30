
# crn_manager.py: control ccc_server and main schedule loop

# from system
from __future__ import division
import socket
import time
import threading
import cPickle
# from current dir
import meta_data
from ccc_server import ccc_server
from control_msg import time_sync_msg





class crn_manager: 

    # store all neighbor sockets info to easily send msg
    neighbor_socks_table = {}   
    # record local start time to calculate virtual time
    start_local_time = 0
    
    ####  flags ####
    # False: not synchronized yet, true: already synchronized
    time_sync_flag = False
    
    #### condition variables ####
    time_sync_con = threading.Condition() 
    
    
    
    def __init__(self, options):
        self.options = options
        self.id = int(options.id)
        
        
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
          
        # wait a while for setting up all connections
        time.sleep(meta_data.connection_setup_time)  
        
        
    def schedule_run(self):
        # synchronize time first
        self.sync_time()
        print self.start_local_time
        time.sleep(100)
        
    def sync_time(self):
        #only source can send time_sync signal
        if self.id == meta_data.source_id:
            # wait a while and let other node get ready for time sync signal
            time.sleep(meta_data.time_sync_setup_time)  
            # start broadcast time sync signal
            self.time_sync_flag = True
            my_time_sync_msg = time_sync_msg(self.time_sync_flag)
            my_time_sync_msg_string = cPickle.dumps(my_time_sync_msg)
            self.broadcast(my_time_sync_msg_string)
        else:
            # all the nodes other than source should get ready and wait for time sync signal
            self.time_sync_con.acquire()
            if self.time_sync_flag == False:
                self.time_sync_con.wait() 
            self.time_sync_con.release()
            
        # record local start time to calculate virtual time
        self.start_local_time = time.time()
        
    def broadcast(self, ctrl_string):
        for i in self.socks_table.keys():
            self.neighbor_socks_table[i].send(ctrl_string)
            
            