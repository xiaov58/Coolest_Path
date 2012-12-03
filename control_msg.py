
        #0: null
        #1: time sync
        
        
class time_sync_msg(control_msg):
    def __init__(self, type, cnt):
        self.type = type
        control_msg.__init__(self, type)
        self.cnt = cnt
