
        #0: null
        #1: time sync
        #2: sensing result info
        #3: reserve
        #4: reserve reply
        #5: free
        
        
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
    def __init__(self, ack):
        self.type = 4
        self.ack = ack

class cts_msg:
    def __init__(self):
        self.type = 5
        

