
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.516, 2.514, 2.512]


# other experiment parameter
init_channel = 1
round = 20               
setup_time = 3               # second
air_time = 1                    # second
min_time = 0.001            # second
yeild_time = 0.01 # second


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
destination_id = 4
neighbour_table =         [[], [2], [1, 3] , [2, 4] , [3]] 
ip_table =                      ['' , '11.0.0.1'  , '11.0.0.2' , '11.0.0.3', '11.0.0.4'] 


# PU info (first item is null to make it easy to count)
pu_id_table = [[] ,   []  ,   [1]  ,  [2, 3] , [] ]
pu_channel = [0, 1, 2, 3]
pu_activity = [
               [], 
               [[19.612, 77.456], [200.171, 300.950]], 
               [[39.872, 79.847], [200.137, 300.646]], 
               [[59.377, 78, 032], [200.137, 300.646]], 
               []
               ]
#pu_activity = [[], [], [], [], []]


