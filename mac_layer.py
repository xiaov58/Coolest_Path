
from control_msg import *
import cPickle
import struct
import time
import sys
import random
import meta_data

class mac_layer:
    def __init__(self, buffer, crn_manager):
        self.pktno = 0
        self.buffer = buffer
        self.crn_manager = crn_manager
            
    def fetch_packge(self):
        self.pktno = self.buffer[0][0]
        pkt_sender_id =  self.buffer[0][1]
        pkt_receiver_id =  self.buffer[0][2]
        data = self.buffer[0][3]
        del self.buffer[0]
        payload =    struct.pack('!H', self.pktno & 0xffff) +\
                            struct.pack('!H', pkt_sender_id & 0xffff) + \
                            struct.pack('!H', pkt_receiver_id & 0xffff) + \
                            data
        return payload
    
    def send(self):
        payload = self.fetch_packge()
        # carrier sense
        delay_range = meta_data.min_time
        while self.crn_manager.role.tb.carrier_sense():
            sys.stderr.write('B')
            time.sleep(delay_range * random.random())
            if delay_range < 0.050:
                delay_range = delay_range * 2       # exponential back-off range
        self.crn_manager.role.tb.txpath.send_pkt(payload, False)
        print "send! pktno %d; channel %d; buffer: %d" % (self.pktno, self.crn_manager.best_channel, len(self.buffer))
        

    def run(self):            
        if self.crn_manager.status == 0 and len(self.buffer) != 0:
            self.crn_manager.status =1
            # reserve receiver
            #print "send rts"
            rts = rts_msg(self.crn_manager.id, self.crn_manager.best_channel)
            rts_string = cPickle.dumps(rts)
            self.crn_manager.socks_table[self.crn_manager.route[self.crn_manager.route.index(self.crn_manager.id) + 1]].send(rts_string)
            # wait for reply
            self.crn_manager.rts_ack_con.acquire()
            self.crn_manager.rts_ack_con.wait()
            print "ready to send at channel %d at %.3f" % (self.crn_manager.best_channel, self.crn_manager.get_virtual_time())
            self.crn_manager.role.tb.set_freq(meta_data.channels[self.crn_manager.best_channel])
            self.crn_manager.rts_ack_con.release()

        if self.crn_manager.status ==1 and len(self.buffer) != 0:
            self.send()
                
        if self.crn_manager.status == 1 and len(self.buffer) == 0:
            self.air_free()
            self.crn_manager.air_con.acquire()
            self.crn_manager.early_free_flag = 0
            # wait at most 1s, if receive the reply for air free msg, wake up immediately
            self.crn_manager.air_con.wait(meta_data.air_time)
            self.crn_manager.air_con.release()
            
            # if alreay early free do not need to free over ccc
            if self.crn_manager.early_free_flag == 0:
                free = free_msg()
                free_string = cPickle.dumps(free)
                print "ccc free at %.3f" % self.crn_manager.get_virtual_time()
                self.crn_manager.socks_table[self.crn_manager.route[self.crn_manager.route.index(self.crn_manager.id) + 1]].send(free_string)
            
            if self.crn_manager.rts_register_flag == 1:
                # direct receive
                rts_ack = rts_ack_msg()
                rts_ack_string = cPickle.dumps(rts_ack)
                self.crn_manager.rts_register_flag = 0
                self.crn_manager.status = 2
                self.crn_manager.role.tb.set_freq(meta_data.channels[self.crn_manager.rts_register_channel])
                self.crn_manager.socks_table[self.crn_manager.rts_register_id].send(rts_ack_string)
            else:
                # give the next_hop highter priority to forward
                time.sleep(meta_data.yeild_forward_time)
                self.crn_manager.status = 0
        
    # special method to solve the air problem that will not happend in realality
    def air_free(self):
        payload =    struct.pack('!H', 0 & 0xffff) +\
                    struct.pack('!H', self.crn_manager.id & 0xffff) + \
                    struct.pack('!H', 0 & 0xffff) 
        # carrier sense
        delay_range = meta_data.min_time
        while self.crn_manager.role.tb.carrier_sense():
            sys.stderr.write('B')
            time.sleep(delay_range * random.random())
            if delay_range < 0.050:
                delay_range = delay_range * 2       # exponential back-off range
                
        self.crn_manager.role.tb.txpath.send_pkt(payload, False)
        print "air free at %.3f" % self.crn_manager.get_virtual_time() 
            
            
