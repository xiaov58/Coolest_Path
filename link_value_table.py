
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
                
    def check_all_updated(self):
        tmp = True
        for i in self.item_set:
            if i.round_cnt == self.round_cnt + 1:
                tmp = tmp and True
            else:
                tmp = tmp and False
        if tmp == True:
            self.round_cnt = self.round_cnt + 1
        return tmp

class link_value_item:
    def __init__(self, neighbour_id, round_cnt):
        self.neighbour_id = neighbour_id
        self.round_cnt = round_cnt
        # temperature for coolest_path
        self.value = [0 for n in range(len(meta_data.channels_freq_table))]