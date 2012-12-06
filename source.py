
# from system
import struct
import sys
import time
import random

# from current dir
import meta_data
from source_block import source_block


class source:

    def __init__(self, options, crn_manager):
        self.options = options
        self.crn_manager = crn_manager
        self.tb = source_block(self.rx_callback, self.options)
        self.tb.rxpath.set_carrier_threshold(options.carrier_threshold)
        self.pktno = 0
        self.next_hop = 2
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        
        while n < nbytes:       
            payload = self.generate_data()
            self.crn_manager.process_con.acquire()
            start = time.time()
            # random backoff, prevent continous sending
            #time.sleep(meta_data.min_delay * meta_data.random_backoff_range * random.random())
            
            if self.crn_manager.process_flag == 0:
                self.crn_manager.process_con.wait()
#            # sense
#            delay = meta_data.min_delay
#            while self.tb.carrier_sensed():
#                sys.stderr.write('B')
#                time.sleep(delay)
#                if delay < 0.050:
#                    delay = delay * 2       # exponential back-off
            
            self.send_pkt(payload)
            n += len(payload)
            end = time.time()
            print "%d; channel %d; time %.3f" % (self.pktno, self.crn_manager.cur_channel , end - start)
            self.pktno += 1
            
            self.crn_manager.process_con.release()
            time.sleep(0.001)
            
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)
        
    def change_channel(self, channel_id):
        self.tb.set_freq()
        
    def generate_data(self):
        # prepare data and pack
        # structure: 
        # |  packet_no   |   source     |   destination |   sender  |   recever    |   data    |
        # |     2 bytes     |   2bytes     |    2bytes       |   2 bytes |   2 bytes     |   ......     |
        pkt_size = int(meta_data.packet_size)
        data = (pkt_size - 10) * chr(self.pktno & 0xff) 
        pkt_sender_id =  int(self.options.id)
        # tempraty routing needed
        pkt_receiver_id = self.next_hop
        payload =    struct.pack('!H', self.pktno & 0xffff) +\
                            struct.pack('!H', meta_data.source_id & 0xffff) + \
                            struct.pack('!H', meta_data.destination_id & 0xffff)  + \
                            struct.pack('!H', pkt_sender_id & 0xffff) + \
                            struct.pack('!H', pkt_receiver_id & 0xffff)  + \
                            data
        return payload
        
    
    def rx_callback(self, ok, payload):
        pass
