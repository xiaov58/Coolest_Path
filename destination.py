
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
        self.links = []
        self.buffer = []
        self.routing_request_log = [] 
        self.log_mask = []
        self.link_number = self.get_link_number()
            
    def get_link_number(self):
        link_number =0
        for i in range(len(meta_data.neighbour_table)):
            link_number += len(meta_data.neighbour_table[i])
        return link_number
        
    def calculate_path(self):
        graph = Graph()
        for i in range(len(self.links)):
            graph.add_edge(self.links[i][0], self.links[i][1], {'cost': self.links[i][2]})
        cost_func = lambda u, v, e, prev_e: e['cost']
        return find_path(graph, meta_data.source_id, meta_data.destination_id, cost_func=cost_func)

    def rx_callback(self, ok, payload):
        if self.crn_manager.status == 2 and len(payload) > 4:
            (pktno, ) = struct.unpack('!H', payload[0:2])
            (pkt_sender_id, ) = struct.unpack('!H', payload[2:4])
            data = payload[4:]
            if ok:
                print "pktno: %d, sender: %d" % (pktno, pkt_sender_id)
                # only count packets from last hop
                if self.crn_manager.route[self.crn_manager.route.index(self.crn_manager.id) -1] == pkt_sender_id:
                    self.received_cnt += 1
            else:
                print "ok: %r \t pktno: %d \t" % (ok, pktno)
            

