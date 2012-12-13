
# default option value
packet_size = 1000           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.516, 4.9006, 4.915]

# other experiment parameter
init_channel = 1
round = 20               
setup_time = 3               # second
air_time = 0.5               # second
min_time = 0.001         # second
yeild_forward_time = 0.01 # second



batch_size = 50
backoff_min = 0.001
backoff_max = 0.050
INF = 100

# sensing PU schedule
time_interval = 5
sensing_time = 0.5

# socket parameter
server_port = 11012
max_client = 5
sock_buffer_size = 1000


# Topology  (first item is null to make it easy to count)
source_id = 1
destination_id = 3
neighbour_table =         [[]      ,   [2]                          ,   [1, 3]                      , [2]                          ] 
ip_table =                       [''     , '11.0.0.1'  , '11.0.0.2'      , '11.0.0.3'] 


# PU info (first item is null to make it easy to count)
pu_id_table =                  [[]      ,   []                           ,   [1]                           ,  [2, 3]                         ]
pu_channel = [0, 1, 2, 3]
#pu_activity = [
#               [], 
#               [[6.612, 48.456], [54.171, 64.950]], 
#               [[14.872, 44.847], [80.137, 100.646]], 
#               [[24.377, 30, 032]]
#               ]
pu_activity = [[], [], [], []]


