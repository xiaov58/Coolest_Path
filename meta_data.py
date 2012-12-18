
# default option value
packet_size = 400           # Byte
carrier_thredshold = -55
bandwidth = 0.2       # MHz
channels = [0, 2.5120, 2.5125, 2.513, 2.5135, 2.514]



# other experiment parameter
init_channel = 1
round = 25               
setup_time = 2               # second
air_time = 1                    # second
min_time = 0.001            # second
yeild_time = 0.02 # second


batch_size = 50
backoff_min = 0.001
backoff_max = 0.050
INF = 100

# sensing PU schedule
time_interval = 2
sensing_time = 0.2

# socket parameter
server_port = 11012
max_client = 10
sock_buffer_size = 1000


# Topology  (first item is null to make it easy to count)
source_id = 1
destination_id = 6
full_duplex_mask =       [0, 0, 1, 0, 1, 0, 1]
neighbour_table =         [[], [2, 4], [1, 3 , 5] , [2, 6] , [1, 5] , [2, 4, 6] , [3, 5]] 
ip_table =                      ['' , '11.0.0.1'  , '11.0.0.2' , '11.0.0.3', '11.0.0.4', '11.0.0.5', '11.0.0.6'] 


# PU info (first item is null to make it easy to count)
pu_channel_num = 5
pu_id_table = [[] ,   []  ,   [1, 2, 3, 4, 5]  ,  [] , [] , [6, 7, 8, 9, 10] , []]
pu_channel = [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
pu_activity = []
