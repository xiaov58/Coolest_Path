
# from system
import struct
import sys

# from current dir
import meta_data

class source:

    def __init__(self, sb, id):
        self.tb = sb;
        self.id = id;
        pass
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        pktno = 0
        pkt_size = int(meta_data.packet_size)
        
        while n < nbytes:
            data = (pkt_size - 4) * chr(pktno & 0xff) 
            pkt_sender_id =  str(self.id)
            
            # tempraty routing needed
            pkt_receiver_id = str(3)
            payload = struct.pack('!H', pktno & 0xffff) + struct.pack('!H', pkt_sender_id & 0xff) + struct.pack('!H', pkt_receiver_id & 0xff)  + data
#            data = (pkt_size - 2) * chr(pktno & 0xff) 
#            payload = struct.pack('!H', pktno & 0xffff) + data
            self.send_pkt(payload)
            n += len(payload)
            print pktno
            pktno += 1
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
        return self.tb.txpath.send_pkt(payload, eof)


        # generate data
        # random wait
        # reserve channel
        # wait confirmation
        # carrier sense
