
# from system
import struct
import sys

# from current dir
import meta_data

class router:

    def __init__(self, sb, id):
        self.tb = sb
        self.id = id
        self.pktno = 0
        self.__n_rcvd = 0
        self.__n_right = 0
        self.header_buffer = []
        self.data_buffer = []
        pass
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        
        while n < nbytes:
            payload = generate_data(self)
            self.send_pkt(payload)
            n += len(payload)
            print pktno
            pktno += 1
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)
        
    # save data to buffer
    def store_data(self):
        pass
        
    # fetch data from buffer and change header
    def fetch_data(self):
        # prepare data and pack
        # structure: 
        # |  packet_No   |   sender  |   recever    |   data    |
        # |     2 Bytes     |   2 Bytes |   2 Bytes     |   ......   |
        pkt_size = int(meta_data.packet_size)
        data = (pkt_size - 6) * chr(self.pktno & 0xff) 
        pkt_sender_id =  int(self.id)
        # tempraty routing needed
        pkt_receiver_id = int(2)
        payload = struct.pack('!H', self.pktno & 0xffff) + struct.pack('!H', pkt_sender_id & 0xffff) + struct.pack('!H', pkt_receiver_id & 0xffff)  + data
        return payload
        
    def rx_callback(self, ok, payload):
        self.__n_rcvd += 1
        (pktno, ) = struct.unpack('!H', payload[0:2])
        (pkt_sender_id, ) = struct.unpack('!H', payload[2:4])
        (pkt_receiver_id, ) = struct.unpack('!H', payload[4:6])
        data = payload[6:]
        if ok:
            self.__n_right += 1
            self.header_buffer.append((pktno, pkt_sender_id, pkt_receiver_id))
            self.data_buffer.append(data)
        print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d \t sender: %d \t receiver: %d" % (ok, pktno, self.__n_rcvd, self.__n_right,  pkt_sender_id,  pkt_receiver_id)
