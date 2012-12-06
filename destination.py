
# from system
import struct

# from current dir
from destination_block import destination_block

class destination:
    
    def __init__(self, options, crn_manager):
            self.__n_rcvd = 0
            self.__n_right = 0
            self.options = options
            self.crn_manager = crn_manager
            self.tb = destination_block(self.rx_callback, self.options)


    def rx_callback(self, ok, payload):
#        self.crn_manager.process_con.acquire()
#        if self.crn_manager.process_flag == 0:
#            self.crn_manager.process_con.wait()
        self.__n_rcvd += 1
        (pktno, ) = struct.unpack('!H', payload[0:2])
        (pkt_source_id, ) = struct.unpack('!H', payload[2:4])
        (pkt_destination_id, ) = struct.unpack('!H', payload[4:6])
        (pkt_sender_id, ) = struct.unpack('!H', payload[6:8])
        (pkt_receiver_id, ) = struct.unpack('!H', payload[8:10])
        if ok:
            self.__n_right += 1
            print "pktno: %d \t n_rcvd: %d \t n_right: %d \t sender: %d \t receiver: %d \t source: %d \t destination: %d" % (pktno, self.__n_rcvd, self.__n_right,  pkt_sender_id,  pkt_receiver_id,  pkt_source_id,  pkt_destination_id)
        else:
            print "ok: %r \t pktno: %d \t" % (ok, pktno)
        #self.crn_manager.process_con.release()

