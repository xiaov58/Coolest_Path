
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
channels = [0, 4.9002, 4.9006, 4.901]

# other experiment parameter
init_channel = 1
round = 20               
min_time = 0.001          # second
setup_time = 3               # second
batch_size = 10
backoff_min = 0.001
backoff_max = 0.050
INF = 100

# sensing PU schedule
time_interval = 1
sensing_time = 0.1

# socket parameter
server_port = 11012
max_client = 5
sock_buffer_size = 1000


# Topology  (first item is null to make it easy to count)
source_id = 1
destination_id = 3
neighbour_table =         [[]      ,   [2]                          ,   [1, 3]                      , [2]                          ] 
ip_table =                       [''     , '128.205.39.104'  , '67.20.206.90'      , '128.205.39.100'] 


# PU info (first item is null to make it easy to count)
pu_id_table =                  [[]      ,   []                           ,   [1]                           ,  [2, 3]                         ]
pu_channel = [0, 1, 2, 3]
pu_activity = [
               [], 
               [[3.612, 24.456], [27.171, 37.950]], 
               [[7.872, 21.847], [46.137, 54.646]], 
               [[12.377, 14, 032]]
               ]


