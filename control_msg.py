
        #0: null
        #1: time sync
        #2: sensing result info
        #3: RTS
        #4: CTS
        
        
class time_sync_msg:
    def __init__(self, cnt):
        self.type = 1
        self.cnt = cnt
        
class sensing_result_msg:
    def __init__(self, sender_id, channel_utilazation_table, channel_mask):
        self.type = 2
        self.sender_id = sender_id
        self.cut = channel_utilazation_table
        self.cm = channel_mask
        
class rts_msg:
    def __init__(self, sender_id, channel_id):
        self.type = 3
        self.sender_id = sender_id
        self.ci = channel_id

class cts_msg:
    def __init__(self):
        self.type = 4

