
# from system
import struct

class destination:
    
    def __init__(self):
            self.__n_rcvd = 0
            self.__n_right = 0

    def rx_callback(self, ok, payload):
        self.__n_rcvd += 1
        pktno = struct.unpack('!H', payload[0:2])
        pkt_dest = struct.unpack('!H', payload[2:4])
        if ok:
            self.__n_right += 1
        print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d pkt_dest %d" % (ok, pktno, self.__n_rcvd, self.__n_right,  pkt_dest)



