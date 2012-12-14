
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
        self.mac_layer_ = mac_layer(self.crn_manager)
        
    def run(self):
        
        while 1:
            self.crn_manager.process_con.acquire()
            if self.crn_manager.process_flag == 0:
                self.crn_manager.process_con.wait()
            self.crn_manager.process_con.release()
            
            if self.crn_manager.status != 2:
                self.mac_layer_.tx_run()
            
            time.sleep(meta_data.min_time)

        
    def rx_callback(self, ok, payload):
        self.mac_layer_.rx_callback(ok, payload)
        
        
