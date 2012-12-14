
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
        self.best_channel = 0       # coolest and available channel for transmiting to  next hop
        self.next_hop = 0
        self.best_links = []
        self.start_local_time = 0
            
        # condition variables
        self.time_sync_con = threading.Condition()  
        self.process_con = threading.Condition()  
        self.rts_ack_con = threading.Condition()  
        self.air_con = threading.Condition()
        
        # flags
        self.time_sync_flag = 0
        self.process_flag = 0
        self.rts_register_flag = 0
        self.rts_register_id = 0
        self.rts_register_channel = 0
        self.error_flag = 0
        self.early_free_flag = 0
        
        # counts
        self.sense_cnt = 0
        self.process_cnt = 0
        self.routing_request_cnt = 0
        self.routing_reply_cnt = 0
        self.routing_error_cnt = 0
        self.routing_request_counter  = 0
        
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
            print "Source: send out %d" % (self.role.mac_layer_.pktno)
        if self.id == meta_data.destination_id:
            print "Destination: recieve %d" % (self.role.received_cnt)
            print self.role.routing_request_log
            print self.role.log_mask
        sys.exit(0)
        
    # Thread priority need
    def sense(self):
        self.process_con.acquire()
        print "sense at virtual time: %.3f" %  (self.get_virtual_time())
        
        if self.sense_cnt == meta_data.round:
            self.exit()
            
        # block process thread before process timer unblock it
        self.process_flag = 0
        self.pseudo_check()
        
        # adjust time and set timer for next round
        time_gap = self.get_virtual_time() - self.sense_cnt * meta_data.time_interval
        self.sense_cnt += 1
        self.sense_timer = threading.Timer(meta_data.time_interval - time_gap, self.sense)
        #print "next in %.3f" % (meta_data.time_interval - time_gap)
        self.sense_timer.daemon = True
        self.sense_timer.start()
        self.process_con.release()
        
    def pseudo_check(self):
        vts = self.sense_cnt * meta_data.time_interval
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
        srm = sensing_result_msg(self.id, self.channel_utilization_table, self.channel_mask)
        srm_string = cPickle.dumps(srm)
        self.broadcast(srm_string) 
        
    def process(self):
        self.process_con.acquire()
        print "process at virtual time: %.3f" % (self.get_virtual_time())

        # update route, not for destination
        if self.id != meta_data.destination_id:
            self.update_routing()
        
        # let main thread run
        if self.error_flag == 0:
            self.process_flag = 1
            self.process_con.notify()
        
        # adjust time and set timer for next round
        time_gap = self.get_virtual_time() - self.process_cnt * meta_data.time_interval
        self.process_cnt += 1
        self.process_timer = threading.Timer(meta_data.time_interval - time_gap + meta_data.sensing_time, self.process)
        self.process_timer.daemon = True
        self.process_timer.start()
        self.process_con.release()
    
    def clear(self):
        self.process_flag = 0
        del self.role.mac_layer_.buffer[:]
        self.status = 0
        # simple way to make main thread sleep, otherwise empty route may cause problem
        time.sleep(meta_data.yeild_time)
        self.route = []
    
    def update_routing(self):
        self.error_flag = 0
        if self.route == []:
            self.error_flag = 1
        else:
            self.set_best_channel()        
            if self.best_channel == 0:
                self.error_flag = 1
   
        if self.error_flag ==1:
            print "routing error"
            # detect routing error, then refuse error  msg from other node
            self.routing_error_cnt += 1
            self.clear()
            
            if self.id != meta_data.source_id:
                err = routing_error_msg(self.routing_error_cnt)
                err_string = cPickle.dumps(err)
                self.broadcast(err_string)
            else:
                self.routing_request_cnt += 1
                self.get_best_links()
                path = [self.id]
                req = routing_request_msg(self.routing_request_cnt, self.best_links)
                req_string = cPickle.dumps(req)
                self.broadcast(req_string)
        
    def get_best_links(self):
        self.best_links = []
        for i in meta_data.neighbour_table[self.id]:
            cost = meta_data.INF
            for j in range(len(meta_data.channels)) :
                if self.link_temp_table[i][j] < cost and self.channel_mask[j] == 1 and self.neighbour_channel_mask[i][j] ==1:
                    cost = self.link_temp_table[i][j]
                    self.role.tb.set_freq(meta_data.channels[j])
            self.best_links.append([self.id, i, cost])       # sender, receiver, cost
        #print self.best_links

    def set_best_channel(self):
        self.best_channel = 0
        self.next_hop = self.route[self.route.index(self.id) + 1]
        for i in meta_data.neighbour_table[self.id]:
            cost = meta_data.INF
            for j in range(len(meta_data.channels)) :
                if self.link_temp_table[i][j] < cost and self.channel_mask[j] == 1 and self.neighbour_channel_mask[i][j] ==1 and i == self.next_hop:
                    self.best_channel = j 
                    cost = self.link_temp_table[i][j]
            
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
        
