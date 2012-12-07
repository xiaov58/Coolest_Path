
# from system
import struct
import sys
import time
import random

# from current dir
import meta_data
from my_top_block import my_top_block

class router:

    def __init__(self, options, crn_manager):
        self.options = options
        self.crn_manager = crn_manager
        self.tb = my_top_block(self.rx_callback, self.options)
        self.tb.rxpath.set_carrier_threshold(options.carrier_threshold)
        self.pktno = 0
        self.__n_rcvd = 0
        self.__n_right = 0
        self.header_buffer = []
        self.data_buffer = []
        # psuedo
        self.next_hop = 3
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        payload = ""
        
        while 1:
            self.crn_manager.process_con.acquire()
            # random backoff, prevent continous receiving
            #time.sleep(meta_data.min_delay * meta_data.random_backoff_range * random.random()) 
            if len(self.data_buffer) == 0 and len(self.header_buffer) == 0:
                pass
            else:
                payload = self.fetch_data()
                if self.crn_manager.process_flag == 0:
                    self.crn_manager.process_con.wait()
                    
#                delay = meta_data.min_delay
#                while self.tb.carrier_sensed():
#                    sys.stderr.write('B')
#                    #print "B"
#                    time.sleep(delay)
#                    if delay < 0.050:
#                        delay = delay * 2       # exponential back-off
                self.send_pkt(payload)
                #print "pktno: %d forwarded" % (self.pktno)
                print "Forward %d; channel %d" % (self.pktno, self.crn_manager.cur_channel)
            self.crn_manager.process_con.release()
            time.sleep(0.001)
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)
        
    # fetch data from buffer and change header
    def fetch_data(self):
        data = self.data_buffer[0]
        del self.data_buffer[0]
        
        self.pktno = self.header_buffer[0][0]
        del self.header_buffer[0]
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
        self.crn_manager.process_con.acquire()
        if self.crn_manager.process_flag == 0:
            self.crn_manager.process_con.wait()
        self.__n_rcvd += 1
        (pktno, ) = struct.unpack('!H', payload[0:2])
        (pkt_source_id, ) = struct.unpack('!H', payload[2:4])
        (pkt_destination_id, ) = struct.unpack('!H', payload[4:6])
        (pkt_sender_id, ) = struct.unpack('!H', payload[6:8])
        (pkt_receiver_id, ) = struct.unpack('!H', payload[8:10])
        data = payload[10:]
        if ok:
            self.__n_right += 1
            # save to buffer
            self.header_buffer.append((pktno, pkt_source_id,  pkt_destination_id,  pkt_sender_id, pkt_receiver_id))
            self.data_buffer.append(data)
            print "pktno: %d \t n_rcvd: %d \t n_right: %d \t sender: %d \t receiver: %d \t source: %d \t destination: %d" % (pktno, self.__n_rcvd, self.__n_right,  pkt_sender_id,  pkt_receiver_id,  pkt_source_id,  pkt_destination_id)
        else:
            print "ok: %r \t pktno: %d \t" % (ok, pktno)
        self.crn_manager.process_con.release()
