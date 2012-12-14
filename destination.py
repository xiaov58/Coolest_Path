
# from system
import struct
import cPickle

# from current dir
import meta_data
from my_top_block import my_top_block
from mac_layer import mac_layer
from dijkstar import Graph, find_path
from control_msg import *

class destination:
    def __init__(self, options, crn_manager):
        self.received_cnt = 0
        self.options = options
        self.crn_manager = crn_manager
        self.tb = my_top_block(self.rx_callback, self.options)
        self.mac_layer_ = mac_layer(self.crn_manager)
        self.links = []
        self.routing_request_cnt = 0
        self.routing_request_log = [] 
        self.log_mask = []
        self.link_number = self.get_link_number()
            
    def get_link_number(self):
        link_number =0
        for i in range(len(meta_data.neighbour_table)):
            link_number += len(meta_data.neighbour_table[i])
        return link_number
        
    def calculate_path(self):
        self.routing_request_log.append(self.crn_manager.get_virtual_time())
        graph = Graph()
        for i in range(len(self.links)):
            graph.add_edge(self.links[i][0], self.links[i][1], {'cost': self.links[i][2]})
        cost_func = lambda u, v, e, prev_e: e['cost']
        #print self.links
        result =  find_path(graph, meta_data.source_id, meta_data.destination_id, cost_func=cost_func)
        route = result[0]
        # clear link list
        del self.crn_manager.role.links[:]
        # check and reply
        if meta_data.INF in result[2]:
            route = []
            self.log_mask.append(0)
        else: 
            self.log_mask.append(1)
        #self.crn_manager.route = route
        return route

    def rx_callback(self, ok, payload):
        if self.mac_layer_.rx_callback(ok, payload) == 1:
            # application layer
            self.received_cnt += 1
            

