
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
        self.role = 0
        self.status = 0         #0: free 1: transmiting 2: reiceving
        self.route = []
        self.route = [1, 2, 3]
        self.best_channel = 0       # coolest and available channel for transmiting to  next hop
        self.start_local_time = 0
            
        # condition variables
        self.time_sync_con = threading.Condition()  
        self.process_con = threading.Condition()  
        self.rts_ack_con = threading.Condition()  
        self.tx_con = threading.Condition()  
        self.rx_con = threading.Condition()  
        
        # flags
        self.time_sync_flag = 0
        self.process_flag = 0
        self.rts_ack_flag = 0
        
        # counts
        self.sense_cnt = 0
        self.process_cnt = 0
        self.routing_request_cnt = 0
        
        # timer
        self.sense_timer = 0
        self.process_timer = 0

        # tables
        self.socks_table = {}
        
        self.channel_mask = [] #1:available 0: not
        for i in range(len(meta_data.channels)) :
            self.channel_mask.append(1)
        self.channel_mask[0] = 0
        
        self.channel_utilization_table = []
        for i in range(len(meta_data.channels)) :
            self.channel_utilization_table.append(0)
        self.channel_utilization_table[0] = 1
        
        self.link_temp_table = {}
        for i in meta_data.neighbour_table[self.id]:
            self.link_temp_table[i] = []
            for j in range(len(meta_data.channels)) :
                self.link_temp_table[i] .append(0)
                
        self.neighbour_channel_mask = {}
        for i in meta_data.neighbour_table[self.id]:
            self.neighbour_channel_mask[i] = []
            for j in range(len(meta_data.channels)) :
                self.neighbour_channel_mask[i] .append(0)
            
        #for calculating utilazation
        self.total_time = 0
        self.active_time_table = []
        for i in range(len(meta_data.channels)) :
            self.active_time_table.append(0)
        
    
    def broadcast(self, ctrl_string):
        str = ctrl_string
        for k in self.socks_table.keys():
            self.socks_table[k].send(str)
        
    def sync_time(self):
        self.time_sync_flag = 1
        tsm = time_sync_msg(self.time_sync_flag)
        tsm_string = cPickle.dumps(tsm)
        self.broadcast(tsm_string)
    
    def get_virtual_time(self):
        return time.time() - self.start_local_time - meta_data.setup_time
    
    def exit(self):
        print "Done !!" 
        if self.id == meta_data.source_id:
            print "Source: send out %d" % (self.role.mac_layer_.pkt_cnt)
        if self.id == meta_data.destination_id:
            print "Destination: recieve %d" % (self.role.pkt_cnt)
            print self.role.routing_request_log
        sys.exit(0)
        
    # Thread priority need
    def sense(self):
        self.process_con.acquire()
        print "sense at virtual time: %.3f" %  (self.get_virtual_time())
        
        if self.sense_cnt == meta_data.round:
            self.exit()
            
        # block process thread
        self.process_flag = 0
    
        # yeild so that process thread can run and wait asap
        time.sleep(meta_data.min_time)

        self.pseudo_check()
        
        # adjust time and set timer for next round
        time_gap = self.get_virtual_time() - self.sense_cnt
        self.sense_cnt += 1
        self.sense_timer = threading.Timer(meta_data.time_interval - time_gap, self.sense)
        self.sense_timer.daemon = True
        self.sense_timer.start()
        self.process_con.release()
        
    def pseudo_check(self):
        vts = self.sense_cnt * 1.0
        self.total_time += 1
        # recover channel_mask to original
        for i in range(len(meta_data.channels)) :
            self.channel_mask[i] = 1
        self.channel_mask[0] = 0

        for i in meta_data.pu_id_table[self.id]:
            for j in meta_data.pu_activity[i]:
                #update channel_utilization_table
                if j[0] < vts < j[1] or j[0] < vts + 0.1 < j[1] :
                    self.channel_mask[meta_data.pu_channel[i]] = 0
                    self.active_time_table[meta_data.pu_channel[i]] += 1
                    
        # recalculate ultilazation table
        for i in range(len(meta_data.channels)) :
            self.channel_utilization_table[i] = self.active_time_table[i]/self.total_time
        self.channel_utilization_table[0] = 1
        
        # broadcast utilazation table to neighbour in order to calculate link temprature
        cum = sensing_result_msg(self.id, self.channel_utilization_table, self.channel_mask)
        cum_string = cPickle.dumps(cum)
        self.broadcast(cum_string) 
        
    def process(self):
        self.process_con.acquire()
        print "process at virtual time: %.3f" % (self.get_virtual_time())
        
        # update route, not for destination
        if self.id != meta_data.destination_id:
            self.update_routing()

        
        # let main thread run
        self.process_flag = 1
        self.process_con.notify()
        
        
        # adjust time and set timer for next round
        time_gap = self.get_virtual_time() - self.process_cnt
        self.process_cnt += 1
        self.process_timer = threading.Timer(meta_data.time_interval - time_gap + meta_data.sensing_time, self.process)
        self.process_timer.daemon = True
        self.process_timer.start()
        self.process_con.release()
        
        
    def update_routing(self):
        best_links = self.get_best_links()
        # if none of the channel can be use, broadcast error so that source will invoke routing request
        if self.best_channel == 0:
            print "route error"            
            # update route
            self.exit()
        
    def get_best_links(self):
        next_hop = self.route[self.route.index(self.id) + 1]
        best_links = {}
        for i in meta_data.neighbour_table[self.id]:
            cost = meta_data.INF
            for j in range(len(meta_data.channels)) :
                if self.link_temp_table[i][j] < cost and self.channel_mask[j] == 1 and self.neighbour_channel_mask[i][j] ==1:
                    if i == next_hop:
                        self.best_channel = j 
                    cost = self.link_temp_table[i][j]
                    self.role.tb.set_freq(meta_data.channels[j])
            best_links[i] = [self.id, i, cost]         # sender, receiver, cost
        return best_links
            
    def run(self):
        # start ccc_server, recieve coming control msg only
        ccc_server_ = ccc_server("ccc_server", self)
        ccc_server_.setDaemon(True)
        ccc_server_.start()
        
         #wait a while for setting up server on all nodes
         #client sock is only used for sending msg out
        time.sleep(meta_data.setup_time)
        
         #connet to server, use dict to store sock list
         #key is the node id, value is the sock descriptor
        for i in meta_data.neighbour_table[self.id]:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( (meta_data.ip_table[i], meta_data.server_port) )
            print sock.recv( meta_data.sock_buffer_size )
            self.socks_table[i] = sock
            
        #only source can send time_sync signal
        if self.id == meta_data.source_id:
           # wait until all connections setup
            time.sleep(meta_data.setup_time)
            self.sync_time()
        
         #wait for time sync
        self.time_sync_con.acquire()
        if self.time_sync_flag == 0:
            self.time_sync_con.wait() 
        self.time_sync_con.release()
        
        self.start_local_time = time.time()
        
        # start timer and make use of interval to build graph

        self.sense_timer = threading.Timer(meta_data.setup_time, self.sense)
        self.sense_timer.daemon = True
        self.sense_timer.start()

        self.process_timer = threading.Timer(meta_data.setup_time + meta_data.sensing_time, self.process)
        self.process_timer.daemon = True
        self.process_timer.start()

        
       # assign diffrent job to diffrent role
       # source
        if self.id == meta_data.source_id:
           # new object and build graph
            self.role = source(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.run()
            self.role.tb.wait()                       # wait for it to finish
        
        # destination
        elif self.id == meta_data.destination_id:
           # new object and build graph
            self.role = destination(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.tb.wait()                       # wait for it to finish
        
        # router
        else:
           # new object and build graph
            self.role = router(self.options, self)
        
            self.role.tb.start()                      # start flow graph
            self.role.run()
            self.role.tb.wait()                       # wait for it to finish
        
