
# from system
import sys
import socket
import time

# from current dir
import meta_data
from ccc_server import ccc_server
from destination import destination
from source import source
from router import router


class crn_manager:

    def __init__(self, options):
        self.options = options
        self.socks_table = {}
        self.channel_utilization_table = {}
        self.time_sync_cnt = 0
        self.role = 0

    def run(self):
        
        # start ccc_server, recieve coming control msg
        ccc_server_ = ccc_server("ccc_server", self.options, self)
        ccc_server_.setDaemon(True)
        ccc_server_.start()
        
        # wait a while for setting up all the node manually, then run ccc_client and connet
        # client sock is only used for sending msg out
        time.sleep(meta_data.server_setup_time)
        
        # use dict to store sock list
        # key is the node id, value is the sock descriptor
        for i in meta_data.neightbour_tup[int(self.options.id)]:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( (meta_data.ip_tup[i], meta_data.server_port) )
            print sock.recv( meta_data.sock_buffer_size )
            self.socks_table[i] = sock
            
        
        # assign diffrent job to diffrent role
        # source
        if meta_data.role_tup[int(self.options.id)] == 'source':
            
            # new object and build graph
            self.role = source(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.sync_time()
            time.sleep(1)
            self.role.run()
            self.role.tb.wait()                       # wait for it to finish
        
        
        # router
        if meta_data.role_tup[int(self.options.id)] == 'router':
            
            # new object and build graph
            self.role = router(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.run()
            self.role.tb.wait()                       # wait for it to finish
        
        # destination
        if meta_data.role_tup[int(self.options.id)] == 'destination':
            
            # new object and build graph
            self.role = destination(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.tb.wait()                       # wait for it to finish
    
