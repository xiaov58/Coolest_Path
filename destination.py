
# from system
import struct

# from current dir
import meta_data
from my_top_block import my_top_block
from dijkstar import Graph, find_path

class destination:
    def __init__(self, options, crn_manager):
        self.received_cnt = 0
        self.options = options
        self.crn_manager = crn_manager
        self.tb = my_top_block(self.rx_callback, self.options)
        self.routing_request_log = [] 
        self.link_number = self.get_link_number()
            
    def get_link_number(self):
        link_number = -1        # minute null element
        for i in range(len(meta_data.neighbour_table)):
            link_number += len(meta_data.neighbour_table[i])
        return link_number

    def rx_callback(self, ok, payload):
#        self.crn_manager.rx_con.acquire()
#        if self.crn_manager.status != 2:
#            self.crn_manager.rx_con.wait()
#        self.crn_manager.rx_con.release()

        if self.crn_manager.status == 2:
            
            (pktno, ) = struct.unpack('!H', payload[0:2])
            (pkt_sender_id, ) = struct.unpack('!H', payload[2:4])
            data = payload[4:]
            if ok:
                print "pktno: %d, sender: %d, status: %d" % (pktno, pkt_sender_id, self.crn_manager.status)
                # only count packets from last hop
                if self.crn_manager.route[self.crn_manager.id -1] == pkt_sender_id:
                    self.received_cnt += 1
            else:
                print "ok: %r \t pktno: %d \t" % (ok, pktno)
            

