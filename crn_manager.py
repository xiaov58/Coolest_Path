
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
        self.role = 0
        self.cur_channel = meta_data.init_channel
        
        #for time sync
        self.time_sync_cnt = 0
        self.time_sync_con = threading.Condition()  
        self.process_con = threading.Condition()  
        self.cts_con = threading.Condition()  
        self.start_local_time = 0
        self.sense_timer = 0
        self.sense_cnt = 0
        self.process_timer = 0
        self.process_cnt = 0
        self.process_flag = 0 

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
        for i in meta_data.neightbour_tup[int(self.options.id)]:
            self.link_temp_table[i] = []
            for j in range(len(meta_data.channels)) :
                self.link_temp_table[i] .append(0)
        self.neighbour_channel_mask = {}
        for i in meta_data.neightbour_tup[int(self.options.id)]:
            self.neighbour_channel_mask[i] = []
            for j in range(len(meta_data.channels)) :
                self.neighbour_channel_mask[i] .append(0)
            
        #for calculating utilazation
        self.total_time = 0
        self.active_time = []
        for i in range(len(meta_data.channels)) :
            self.active_time.append(0)
        
    
    def broadcast(self, ctrl_string):
        str = ctrl_string
        for k in self.socks_table.keys():
            self.socks_table[k].send(str)
        
    def sync_time(self):
        self.time_sync_cnt += 1
        tsm = time_sync_msg(self.time_sync_cnt)
        tsm_string = cPickle.dumps(tsm)
        self.broadcast(tsm_string)
    
    # Thread priority need
    def sense(self):
        virtual_time_stamp_ = time.time() - self.start_local_time - meta_data.setup_time
        print "acquire at virtual time: %.3f" % virtual_time_stamp_
        self.process_con.acquire()
        virtual_time_stamp = time.time() - self.start_local_time - meta_data.setup_time
        print "sense at virtual time: %.3f" % virtual_time_stamp

        # block process thread
        self.process_flag = 0
        self.process_con.release()
        # sleep so that process thread can run and wait as soon as possible
        time.sleep(0.001)
        self.sense_cnt += 1
        self.pseudo_check(virtual_time_stamp_)
        
        # adjust time
        new_virtual_time_stamp = time.time() - self.start_local_time - meta_data.setup_time
        time_gap = new_virtual_time_stamp - self.sense_cnt * 1 + 1
        self.sense_timer = threading.Timer(meta_data.time_interval - time_gap, self.sense)
        self.sense_timer.daemon = True
        self.sense_timer.start()
        
    def pseudo_check(self, virtual_time_stamp):
        vts = virtual_time_stamp
        self.total_time += 1
        # recover channel_mask
        for i in range(len(meta_data.channels)) :
            self.channel_mask[i] = 1
        self.channel_mask[0] = 0

        for i in meta_data.pu_id_tup[int(self.options.id)]:
            for j in meta_data.pu_activity[int(i)]:
                #update channel_utilization_table
                if j[0] < vts < j[1] or j[0] < vts + 0.1 < j[1] :
                    self.channel_mask[int(meta_data.pu_channel[int(i)])] = 0
                    self.active_time[int(meta_data.pu_channel[int(i)])] += 1
        
        # recalculate ultilazation table
        for i in range(len(meta_data.channels)) :
            self.channel_utilization_table[i] = self.active_time[i]/self.total_time
        
#        print self.channel_mask
#        print self.active_time
        # broadcast utilazation table to neighbour in order to calculate link temprature
        cum = sensing_result_msg(self.options.id, self.channel_utilization_table, self.channel_mask)
        cum_string = cPickle.dumps(cum)
        self.broadcast(cum_string)
        
    def process(self):
        self.process_con.acquire()
        virtual_time_stamp = time.time() - self.start_local_time - meta_data.setup_time
        print "process at virtual time: %.3f" % virtual_time_stamp
        
        print self.neighbour_channel_mask
        print self.link_temp_table
        self.process_cnt += 1
        # need modification
        if  (self.process_cnt - 1)%meta_data.hop_cnt == (int(self.options.id) - 1):
            start = time.time()
            self.process_flag = 1
            self.set_channel(int(self.role.next_hop))
            # reserve receiving channel
            rts = rts_msg(int(self.options.id), self.cur_channel)
            rts_string = cPickle.dumps(rts)
            self.socks_table[self.role.next_hop].send(rts_string)
            #wait for cts
            self.cts_con.acquire()
            self.cts_con.wait()
            self.cts_con.release()
            end = time.time()
            print "preprocess time %.3f" % (end - start)
            
            self.process_con.notify()
        
        # adjust time
        new_virtual_time_stamp = time.time() - self.start_local_time - meta_data.setup_time
        time_gap = new_virtual_time_stamp - self.process_cnt * 1 + 1
        self.process_timer = threading.Timer(meta_data.time_interval - time_gap + meta_data.sensing_time, self.process)
        self.process_timer.daemon = True
        self.process_timer.start()
        self.process_con.release()
        
    def set_channel(self, next_top):
        channel_id = 0
        temprature = 1
        for i in range(len(meta_data.channels)) :
            if self.link_temp_table[next_top][i] < temprature and self.channel_mask[i] == 1 and self.neighbour_channel_mask[next_top][i] ==1:
                self.cur_channel = i 
                temprature = self.link_temp_table[next_top][i]
                self.role.tb.set_freq(meta_data.channels[i])
        if self.cur_channel == 0:
            # all channel not available
            # send routing request
            print "Route Request"
            pass
            
    
    def get_coolest_channel(self, next_top):
        channel_id = 0
        temprature = 1
        for i in range(len(meta_data.channels)) :
            if link_temp_table[next_top][i] < temprature:
                temprature = self.link_temp_table[next_top][i]
                channel_id = i
        return (channel_id, temprature)

    def run(self):
        
        # start ccc_server, recieve coming control msg
        ccc_server_ = ccc_server("ccc_server", self.options, self)
        ccc_server_.setDaemon(True)
        ccc_server_.start()
        
         #wait a while for setting up all the node manually, then run ccc_client and connet
         #client sock is only used for sending msg out
        time.sleep(meta_data.setup_time)
        
         #use dict to store sock list
         #key is the node id, value is the sock descriptor
        for i in meta_data.neightbour_tup[int(self.options.id)]:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( (meta_data.ip_tup[i], meta_data.server_port) )
            print sock.recv( meta_data.sock_buffer_size )
            self.socks_table[i] = sock
            
        #source begin to send time_sync signal
        if meta_data.role_tup[int(self.options.id)] == 'source':
           # wait for connections setup
            time.sleep(meta_data.setup_time)
            self.sync_time()
        
         #wait for time sync
        self.time_sync_con.acquire()
        if self.time_sync_cnt == 0:
            self.time_sync_con.wait() 
        self.time_sync_con.release()
        
        self.start_local_time = time.time()
        
        
        # make use of interval to build graph
        print time.time()
        self.sense_timer = threading.Timer(meta_data.setup_time, self.sense)
        self.sense_timer.daemon = True
        self.sense_timer.start()
        print time.time()
        self.process_timer = threading.Timer(meta_data.setup_time + meta_data.sensing_time, self.process)
        self.process_timer.daemon = True
        self.process_timer.start()
        print time.time()
        
        #time.sleep(100)
       # assign diffrent job to diffrent role
       # source
        if meta_data.role_tup[int(self.options.id)] == 'source':
            
           # new object and build graph
            self.role = source(self.options, self)
        
            self.role.tb.start()                      # start flow graph
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
    
