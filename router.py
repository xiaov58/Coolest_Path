
# from system
import struct
import sys
import threading
import time
import random

# from current dir
import meta_data
from router_block import router_block

con = threading.Condition()

class router:

    def __init__(self, options):
        self.options = options
        self.tb = router_block(self.rx_callback, self.options)
        self.pktno = 0
        self.__n_rcvd = 0
        self.__n_right = 0
        self.header_buffer = []
        self.data_buffer = []
        pass
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        
        while 1:
            # check if buffer is empry, buffer is critical section
            if con.acquire():
                if len(self.data_buffer) == 0 and len(self.header_buffer) == 0:
                    con.wait()
                else:
                    payload = self.fetch_data()
                    con.release()
                    
            # random backoff, prevent continous receiving
            time.sleep(meta_data.min_daley * random_backoff_range * random.random())
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
            print "pktno: %d forwarded" % (self.pktno)
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
        pkt_receiver_id = int(3)
        payload =    struct.pack('!H', self.pktno & 0xffff) +\
                            struct.pack('!H', meta_data.source_id & 0xffff) + \
                            struct.pack('!H', meta_data.destination_id & 0xffff)  + \
                            struct.pack('!H', pkt_sender_id & 0xffff) + \
                            struct.pack('!H', pkt_receiver_id & 0xffff)  + \
                            data
        print "pktno: %d fetched" % (self.pktno)
        # check if the buffer becomes empty
        return payload
        
    def rx_callback(self, ok, payload):
        self.__n_rcvd += 1
        (pktno, ) = struct.unpack('!H', payload[0:2])
        (pkt_source_id, ) = struct.unpack('!H', payload[2:4])
        (pkt_destination_id, ) = struct.unpack('!H', payload[4:6])
        (pkt_sender_id, ) = struct.unpack('!H', payload[6:8])
        (pkt_receiver_id, ) = struct.unpack('!H', payload[8:10])
        data = payload[10:]
        if ok:
            self.__n_right += 1
            # save to buffer, buffer is critical section
            if con.acquire():
                self.header_buffer.append((pktno, pkt_source_id,  pkt_destination_id,  pkt_sender_id, pkt_receiver_id))
                self.data_buffer.append(data)
                con.notify()
                con.release()
            print "pktno: %d \t n_rcvd: %d \t n_right: %d \t sender: %d \t receiver: %d \t source: %d \t destination: %d" % (pktno, self.__n_rcvd, self.__n_right,  pkt_sender_id,  pkt_receiver_id,  pkt_source_id,  pkt_destination_id)
        else:
            print "ok: %r \t pktno: %d \t" % (ok, pktno)
