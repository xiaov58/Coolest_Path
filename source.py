
# from system
import struct
import sys

# from current dir
import meta_data

class source:

    def __init__(self, sb):
        self.tb = sb;
        pass
        
    def run(self):
        n = 0
        nbytes = int(1e6 * meta_data.total_size)
        pktno = 0
        pkt_size = int(meta_data.packet_size)
        
        while n < nbytes:
            data = (pkt_size - 2) * chr(pktno & 0xff) 
            payload = struct.pack('!H', pktno & 0xffff) + data
            self.send_pkt(payload)
            n += len(payload)
            sys.stderr.write('.')
            pktno += 1
        self.send_pkt(eof=True)

    def send_pkt(self, payload='', eof=False):
                
        # generate data
        # random wait
        # reserve channel
        # wait confirmation
        # carrier sense
        return self.tb.txpath.send_pkt(payload, eof)
