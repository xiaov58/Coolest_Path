
# control msg for time synchronization
class time_sync_msg:
    def __init__(self, time_sync_flag):
        self.type = 1
        
class sensing_result_msg:
    def __init__(self, sender_id, channel_util_table, channel_mask_table, round_cnt):
        self.type = 2
        self.sender_id = sender_id
        self.channel_util_table = channel_util_table
        self.channel_mask_table = channel_mask_table
        self.round_cnt = round_cnt
        
class rts_msg:
    def __init__(self, sender_id, channel_id):
        self.type = 3
        self.sender_id = sender_id
        self.channel_id = channel_id

class rts_ack_msg:
    def __init__(self):
        self.type = 4
        
class ccc_free_msg:
    def __init__(self, sender_id):
        self.type = 5
        self.sender_id = sender_id
        
class routing_request_msg:
    def __init__(self, routing_request_cnt, path, links):
        self.type = 6
        self.routing_request_cnt = routing_request_cnt
        self.path = path
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
        
class air_free_reply:
    def __init__(self):
        self.type = 9
