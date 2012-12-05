
        #0: null
        #1: time sync
        #2: channel_utilazation info
        
        
class time_sync_msg:
    def __init__(self, type, cnt):
        self.type = type
        self.cnt = cnt
        
class channel_utilazation_msg:
    def __init__(self, type, sender_id, channel_utilazation_table):
        self.type = type
        self.sender_id = sender_id
        self.cut = channel_utilazation_table
