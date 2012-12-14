
        
class time_sync_msg:
    def __init__(self, time_sync_flag):
        self.type = 1
        self.time_sync_flag = time_sync_flag
        
class sensing_result_msg:
    def __init__(self, sender_id, channel_utilization_table, channel_mask):
        self.type = 2
        self.sender_id = sender_id
        self.channel_utilization_table = channel_utilization_table
        self.channel_mask = channel_mask
        
class rts_msg:
    def __init__(self, sender_id, channel_id):
        self.type = 3
        self.sender_id = sender_id
        self.channel_id = channel_id

class rts_ack_msg:
    def __init__(self):
        self.type = 4

class cts_msg:
    def __init__(self):
        self.type = 5
        
class routing_request_msg:
    def __init__(self, routing_request_cnt, links):
        self.type = 6
        self.routing_request_cnt = routing_request_cnt
        self.links = links
        
class routing_reply_msg:
    def __init__(self,routing_reply_cnt,  route):
        self.type = 7
        self.routing_reply_cnt = routing_reply_cnt
        self.route = route
        
class routing_error_msg:
    def __init__(self, routing_error_cnt):
        self.type = 8
        self.routing_error_cnt = routing_error_cnt
