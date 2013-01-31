
# link_value_table.py: record all the link info of connection with neighbors

import meta_data

class link_value_table:
    def __init__(self, node_id, crn_manager):
        self.crn_manager = crn_manager
        # round cnt of the whole table
        # compare with the round_cnt of crn_manager in order to label if the data is updated in each round
        self.round_cnt = 0
        self.id = node_id
        self.item_num = len(meta_data.neighbour_table[self.id])
        self.item_set = set()
        for i in range(self.item_num):
            my_link_value_item = link_value_item(meta_data.neighbour_table[self.id][i], self.round_cnt)
            self.item_set.add(my_link_value_item)
        
    def update_item(self, sender_id, sender_channel_util_table, sender_channel_mask_table, sender_round_cnt):
        all_update_flag = True
        for i in self.item_set:
            if i.neighbour_id == sender_id:
                i.round_cnt = sender_round_cnt
                temperature = [0 for n in range(len(meta_data.channels_freq_table))]
                for j in range(len(meta_data.channels_freq_table)):
                    # calculate temperature
                    temperature[j] = 1-(1-self.crn_manager.channel_util_table[j])*(1-sender_channel_util_table[j])
                    # apply mask
                    if self.crn_manager.channel_mask_table[j] == 1 or sender_channel_mask_table[j] == 1:
                        i.value[j] = meta_data.INF
                    else:
                        i.value[j] = temperature[j]
            # check if all the items is updated by the way
            if i.round_cnt == self.round_cnt + 1:
                all_update_flag = all_update_flag and True
            else:
                all_update_flag = all_update_flag and False
        if all_update_flag == True:
            self.round_cnt = self.round_cnt + 1
            self.crn_manager.link_table_update_con.acquire()
            self.crn_manager.link_table_update_flag = True
            self.crn_manager.link_table_update_con.notify() 
            self.crn_manager.link_table_update_con.release()
    
    def select_best_link(self):
        best_link = []
        for i in self.item_set:
            cost = meta_data.INF
            channel_number = None
            for j in range(len(meta_data.channels_freq_table)) :
                # select lowest temperature
                if i.value[j] < cost:
                    cost = i.value[j]
                    channel_number = j
            best_link.append([self.id, i.neighbour_id, cost, channel_number])       # [sender_id, receiver_id, cost, channel_number]
        return best_link
        

class link_value_item:
    def __init__(self, neighbour_id, round_cnt):
        self.neighbour_id = neighbour_id
        self.round_cnt = round_cnt
        # temperature for coolest_path
        self.value = [0 for n in range(len(meta_data.channels_freq_table))]
        