
# from system
import struct
import sys
import time
import random

# from current dir
import meta_data
from mac_layer import mac_layer
from my_top_block import my_top_block

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
            
            self.crn_manager.tx_con.acquire()
            if self.crn_manager.status == 2:
                self.crn_manager.tx_con.wait()
            self.crn_manager.tx_con.release()
            
            self.mac_layer_.run()
            
            self.crn_manager.process_con.release()
            #yeild
            time.sleep(meta_data.min_time)

        
    def rx_callback(self, ok, payload):
        self.crn_manager.process_con.acquire()
        if self.crn_manager.process_flag == 0:
            print "wait"
            self.crn_manager.process_con.wait()
        
#        self.crn_manager.rx_con.acquire()
#        if self.crn_manager.status != 2:
#            self.crn_manager.rx_con.wait()
#            print "wait"
#        self.crn_manager.rx_con.release()


        (pktno, ) = struct.unpack('!H', payload[0:2])
        (pkt_sender_id, ) = struct.unpack('!H', payload[2:4])
        data = payload[4:]
        if ok:
            if len(self.buffer) == 0:
                self.crn_manager.buffer_con.acquire()
                self.crn_manager.buffer_con.notify()
                self.crn_manager.buffer_con.release()
            # save to buffer, change sender_id
            self.buffer.append([pktno, int(self.options.id), data])
            print "pktno: %d, sender: %d" % (pktno, pkt_sender_id)
        else:
            print "ok: %r \t pktno: %d \t" % (ok, pktno)
        self.crn_manager.process_con.release()
