# Options value
init_channel = 1
source_id = 1
destination_id = 3
packet_size = 400           # Byte
total_size = 1                  # Mega Byte
default_carrier_thredshold = -60
min_delay = 0.001          # unit: second
random_backoff_range = 100 #ms
setup_time = 3
time_interval = 1
time_adjust_runs = 10
sensing_time = 0.1
server_port = 11012
max_client = 5
hop_cnt  = 2
sock_buffer_size = 1000

channels = [0, 4.5002, 4.5004, 4.5006]

# Topology
# first item is null to make it easy to count
role_tup =                    [''      , 'source'                 , 'router'                 , 'destination'      ]
neightbour_tup =         [[]      ,   [2]                          ,   [1, 3]                      , [2]                          ] 
ip_tup =                       [''      , '128.205.39.104'  , '67.20.206.90'      , '128.205.39.100'] 
pu_id_tup =                  [[]      ,   []                           ,   [1]                           ,  [2]                         ]

# PU info
pu_activity = [
               [], 
               [[1.612, 24.456], [27.171, 37.950]], 
               [[5.872, 21.847], [46.137, 54.646]]
               ]
pu_channel = [0, 1, 2]

