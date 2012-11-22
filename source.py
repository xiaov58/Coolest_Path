
# from system
import struct
import sys
import time
import random

# from current dir
import meta_data
from source_block import source_block

class source:

    def __init__(self, options):
        self.options = options
        self.tb = source_block(self.rx_callback, self.options)
        self.pktno = 0
        pass
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        
        while n < nbytes:
            payload = self.generate_data()
            
            # random backoff, prevent continous receiving
            #time.sleep(meta_data.min_delay * meta_data.random_backoff_range * random.random())
            # RTS
            # CTS
            # sense
            delay = meta_data.min_delay
            while self.tb.carrier_sensed():
                sys.stderr.write('B')
                time.sleep(delay)
                if delay < 0.050:
                    delay = delay * 2       # exponential back-off
            
            self.send_pkt(payload)
            n += len(payload)
            print self.pktno
            self.pktno += 1
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)
        
    def generate_data(self):
        # prepare data and pack
        # structure: 
        # |  packet_no   |   source     |   destination |   sender  |   recever    |   data    |
        # |     2 bytes     |   2bytes     |    2bytes       |   2 bytes |   2 bytes     |   ......     |
        pkt_size = int(meta_data.packet_size)
        data = (pkt_size - 10) * chr(self.pktno & 0xff) 
        pkt_sender_id =  int(self.options.id)
        # tempraty routing needed
        pkt_receiver_id = int(2)
        payload =    struct.pack('!H', self.pktno & 0xffff) +\
                            struct.pack('!H', meta_data.source_id & 0xffff) + \
                            struct.pack('!H', meta_data.destination_id & 0xffff)  + \
                            struct.pack('!H', pkt_sender_id & 0xffff) + \
                            struct.pack('!H', pkt_receiver_id & 0xffff)  + \
                            data
        return payload
        


    def rx_callback(self, ok, payload):
        pass
