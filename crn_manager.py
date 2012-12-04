
# from system
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
        self.socks_table = {}
        self.channel_utilization_table = {}
        self.role = 0
        self.time_sync_cnt = 0
        self.time_sync_con = threading.Condition()  
    
    def broadcast(self, str):
        for k in self.socks_table.keys():
            self.socks_table[k].send(str)
        
    def sync_time(self):
        self.time_sync_cnt += 1
        tsm = time_sync_msg(1, self.time_sync_cnt)
        tsm_string = cPickle.dumps(tsm)
        broadcast(tsm_string)

    def run(self):
        
        # start ccc_server, recieve coming control msg
        ccc_server_ = ccc_server("ccc_server", self.options, self)
        ccc_server_.setDaemon(True)
        ccc_server_.start()
        
        # wait a while for setting up all the node manually, then run ccc_client and connet
        # client sock is only used for sending msg out
        time.sleep(meta_data.setup_time)
        
        # use dict to store sock list
        # key is the node id, value is the sock descriptor
        for i in meta_data.neightbour_tup[int(self.options.id)]:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( (meta_data.ip_tup[i], meta_data.server_port) )
            print sock.recv( meta_data.sock_buffer_size )
            self.socks_table[i] = sock
            

        
        # source begin to send time_sync signal
        if meta_data.role_tup[int(self.options.id)] == 'source':
            # wait for connections setup
            time.sleep(meta_data.setup_time)
            print "time sync"
            self.sync_time()
        
        # wait for time sync
        self.time_sync_con.acquire()
        if self.time_sync_cnt == 0:
            print "wait"
            self.time_sync_con.wait() 
        self.time_sync_con.release()
        
        print "Timer start at local time:",time.time()
        time.sleep(100)
        
#       # assign diffrent job to diffrent role
#       # source
#        if meta_data.role_tup[int(self.options.id)] == 'source':
#            
#           # new object and build graph
#            self.role = source(self.options, self)
#        
#            self.role.tb.start()                      # start flow graph
#            self.role.run()
#            self.role.tb.wait()                       # wait for it to finish
#        
#        
#       # router
#        if meta_data.role_tup[int(self.options.id)] == 'router':
#            
#           # new object and build graph
#            self.role = router(self.options, self)
#        
#            self.role.tb.start()                      # start flow graph
#            self.role.run()
#            self.role.tb.wait()                       # wait for it to finish
#        
#       # destination
#        if meta_data.role_tup[int(self.options.id)] == 'destination':
#            
#           # new object and build graph
#            self.role = destination(self.options, self)
#        
#            self.role.tb.start()                      # start flow graph
#            self.role.tb.wait()                       # wait for it to finish
    
