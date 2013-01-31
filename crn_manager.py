
# crn_manager.py: control ccc_server and main schedule loop

# from system
from __future__ import division
import socket
import time
import threading
import cPickle
import sys
# from current dir
import meta_data
from ccc_server import ccc_server
from link_value_table import link_value_table
from control_msg import time_sync_msg, sensing_result_msg



class crn_manager:     
    def __init__(self, options):
        self.options = options
        self.id = int(options.id)
        
        # record route
        self.route = []
        # store all neighbor sockets info to easily send msg
        # key is the node id, value is the sock descriptor
        self.neighbor_socks_table = {}   
        # record local start time to calculate virtual time
        self.start_local_time = 0
        # record the round_cnt to check if should exit and calculate channel utilization
        self.round_cnt = 0
        # record channel_info to check if the channel info is updated
        self.channel_info_cnt = 0
        # record active time for each channel to calculate channel utilization, initial values are 0
        self.channel_busytime_table = [0 for n in range(len(meta_data.channels_freq_table))]
        # record channel utilization info to exchange and calculate temperature, initial values are 0
        self.channel_util_table = [0 for n in range(len(meta_data.channels_freq_table))]
        # record if channel is available in current round, so need to be refresh every round
        # initial values are 0, 0 means available, 1 means unavailable
        self.channel_mask_table = [0 for n in range(len(meta_data.channels_freq_table))]
        # buffer the sensing_result_msg from neighbor when myself's channel info is not updated yet
        self.sensing_result_msg_buffer = set() 
        # sensing_result_msg_buffer_lock: make sure thread safety
        self.sensing_result_msg_buffer_lock = threading.Lock()
        
        ####  flags ####
        # False: not synchronized yet, true: already synchronized
        self.time_sync_flag = False
        self.link_table_update_flag = False
        
        #### condition variables ####
        self.time_sync_con = threading.Condition() 
        self.link_table_update_con = threading.Condition()
        
        
        # must place it at the bottom of __init__ ,because of the nature of script language 
        self.my_link_value_table = link_value_table(self.id, self)
            
        
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
        
        # start timer and get ready to enter main loop
        # main loop is the third thread
        # use block and unblock to let main_loop and schedule_run perform as one
        self.sense_timer = threading.Timer(meta_data.block_setup_time, self.main_loop)
        self.sense_timer.daemon = True
        self.sense_timer.start()
        
        # make use of first interval to build graph
        time.sleep(100)
        
        
    def main_loop(self):
        # check: exit if experiment time is over
        self.round_cnt += 1
        if self.get_run_time() > meta_data.experiment_total_time:
            self.exit()
        
        # block Tx/Rx
        
        # pseudo sensing here, do nothing actually, need to adjust sleep time
        sensing_start_time = self.get_virtual_time()
        print sensing_start_time
        time.sleep(meta_data.pu_sensing_time - self.get_adjust_time())
        sensing_end_time = self.get_virtual_time()
        print sensing_end_time
        
        # check pseudo sensing result 
        self.update_channel_info(sensing_start_time, sensing_end_time)
        
        # exchange sensing result with neighbors
        my_sensing_result_msg = sensing_result_msg(self.id, 
                                                   self.channel_util_table, 
                                                   self.channel_mask_table, 
                                                   self.round_cnt)
        my_sensing_result_msg_string = cPickle.dumps(my_sensing_result_msg)
        self.broadcast(my_sensing_result_msg_string)
        
        # make sure that link_vlaue_table is completely updated
        self.link_table_update_con.acquire()
        if self.link_table_update_flag == False:
            self.link_table_update_con.wait() 
        self.link_table_update_flag = False
        self.link_table_update_con.release()
        
        # select best channel, and check if the route still hold for current node
        best_link_table = self.my_link_value_table.select_best_link()
        print best_link_table
        
        
        # process is done set timer to enter loop again
        self.sense_timer = threading.Timer(meta_data.round_time - self.get_adjust_time(), self.main_loop )
        self.sense_timer.daemon = True
        self.sense_timer.start()
        
        # unblock Tx/Rx
        
    
    def update_channel_info(self, start, end):
        
        # check if the PU is active in this sensing slot
        for i in meta_data.pu_id_table[self.id]:
            for j in meta_data.pu_activity[i]:
                # update channel_busytime_table and channel mask
                if j[0] < start < j[1] or j[0] < end < j[1] or j[0] < start < end < j[1]:
                    self.channel_mask_table[(i-1)%len(meta_data.channels_freq_table)] = 1
                    self.channel_busytime_table[(i-1)%len(meta_data.channels_freq_table)] += meta_data.round_time
        # update channel utilization table
        for i in range(len(meta_data.channels_freq_table)) :
            self.channel_util_table[i] = self.channel_busytime_table[i]/self.get_run_time()

        self.sensing_result_msg_buffer_lock.acquire()
        # if there is any msg in buffer, check them out
        for i in self.sensing_result_msg_buffer:
            self.my_link_value_table.update_item(i.sender_id, 
                                                 i.channel_util_table, 
                                                 i.channel_mask_table,
                                                 i.round_cnt)
        self.sensing_result_msg_buffer.clear()
        # indicate the channel info is updated
        self.channel_info_cnt += 1
        self.sensing_result_msg_buffer_lock.release()
                    
        
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
        for i in self.neighbor_socks_table.keys():
            self.neighbor_socks_table[i].send(ctrl_string)
    
    def get_virtual_time(self):
        return time.time() - self.start_local_time - meta_data.block_setup_time

    def get_run_time(self):
        return self.round_cnt * meta_data.round_time
    
    def get_adjust_time(self):
        return self.get_virtual_time() - (self.round_cnt - 1) * meta_data.round_time
    
    def exit(self):
        print "Done !!" 
        # print all the experiment result
        sys.exit(0)
            
            