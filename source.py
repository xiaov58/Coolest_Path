
# from system
import struct
import sys
import time
import random

# from current dir
import meta_data
from my_top_block import my_top_block
from mac_layer import mac_layer


class source:

    def __init__(self, options, crn_manager):
        self.options = options
        self.crn_manager = crn_manager
        self.tb = my_top_block(self.rx_callback, self.options)
        self.tb.rxpath.set_carrier_threshold(options.carrier_threshold)
        self.pktno = 0
        self.buffer = []
        self.mac_layer_ = mac_layer(self.buffer, self.crn_manager)
        
    def run(self):
        while 1:       
            # app layer: fill the buffer once it is empty
            # do not need to lock app layer during sensing, because app layer do not use USRP
            if len(self.buffer) == 0 and self.crn_manager.status == 0:
                for i in range(meta_data.batch_size):
                    payload = self.generate_pakcage()
                    
            self.crn_manager.process_con.acquire()
            if self.crn_manager.process_flag == 0:
                self.crn_manager.process_con.wait()
            self.crn_manager.process_con.release()
            
#            self.crn_manager.tx_con.acquire()
#            if self.crn_manager.status == 2:
#                self.crn_manager.tx_con.wait()
#            self.crn_manager.tx_con.release()
#            
#            self.mac_layer_.run()
            time.sleep(meta_data.min_time)
            if self.crn_manager.status != 2:
                self.mac_layer_.run()

            
            #yeild
            time.sleep(meta_data.min_time)
        
    def generate_pakcage(self):
        # prepare data and save to buffer
        # structure: 
        # |  packet_no   |   sender  |   data    |
        # |     2 bytes     |   2 bytes |   ......     |
        pkt_size = int(meta_data.packet_size)
        self.pktno += 1
        pkt_sender_id =  int(self.options.id)
        data = (pkt_size - 6) * chr(self.pktno & 0xff) 
        self.buffer.append([self.pktno, pkt_sender_id, data])
        
    
    def rx_callback(self, ok, payload):
        pass
