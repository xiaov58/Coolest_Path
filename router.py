
# from system
import struct
import sys
import time
import random
import cPickle

# from current dir
import meta_data
from mac_layer import mac_layer
from my_top_block import my_top_block
from control_msg import *

class router:

    def __init__(self, options, crn_manager):
        self.options = options
        self.crn_manager = crn_manager
        self.tb = my_top_block(self.rx_callback, self.options)
        self.tb.rxpath.set_carrier_threshold(options.carrier_threshold)
        self.buffer = []
        self.mac_layer_ = mac_layer(self.buffer, self.crn_manager)
        
    def run(self):
        
        while 1:
            self.crn_manager.process_con.acquire()
            if self.crn_manager.process_flag == 0:
                self.crn_manager.process_con.wait()
            self.crn_manager.process_con.release()
            
            if self.crn_manager.status != 2:
                self.mac_layer_.run()
            
            time.sleep(meta_data.min_time)

        
    def rx_callback(self, ok, payload):
        if self.crn_manager.status == 2:
            if ok:
                (pktno, ) = struct.unpack('!H', payload[0:2])
                (pkt_sender_id, ) = struct.unpack('!H', payload[2:4])
                (pkt_receiver_id, ) = struct.unpack('!H', payload[4:6])
                data = payload[6:]
                if self.crn_manager.id == pkt_receiver_id:
                    if pktno == 0:
                        print "get air free from %d at %.3f" % (pkt_sender_id, self.crn_manager.get_virtual_time())
                        self.crn_manager.status = 0
                        # send air free reply
                        afr = air_free_reply()
                        afr_string = cPickle.dumps(afr)
                        self.crn_manager.socks_table[pkt_sender_id].send(afr_string)
                    else:
                        print "received! pktno: %d, from %d to %d" % (pktno, pkt_sender_id, pkt_receiver_id)
                        self.buffer.append([pktno, self.crn_manager.id, self.crn_manager.next_hop, data])
                else:
                    print "overhear! pktno: %d, from %d to %d" % (pktno, pkt_sender_id, pkt_receiver_id)
            else:
                (pktno, ) = struct.unpack('!H', payload[0:2])
                print "ok: %r \t pktno: %d \t" % (ok, pktno)
        
        
