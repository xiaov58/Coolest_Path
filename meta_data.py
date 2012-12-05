# Options value
init_channel = 1
source_id = 1
destination_id = 3
packet_size = 400           # Byte
total_size = 1                  # Mega Byte
default_carrier_thredshold = -50
min_delay = 0.001          # unit: second
random_backoff_range = 50 #ms
setup_time = 5
time_interval = 1
time_adjust_runs = 10
sensing_time = 0.1
server_port = 11012
max_client = 5
sock_buffer_size = 1000

channels = [0, 4.915, 4.917, 4.919]

# Topology
# first item is null to make it easy to count
role_tup =                    [''      , 'source'                 , 'router'                 , 'destination'      ]
neightbour_tup =         [[]      ,   [2]                          ,   [1, 3]                      , [2]                          ] 
ip_tup =                       [''      , '128.205.39.104'  , '67.20.206.90'      , '128.205.39.100'] 
pu_id_tup =                  [[]      ,   []                           ,   [1]                           ,  [2]                         ]

# PU info
pu_activity = [
               [], 
               [[5.872, 21.847], [46.137, 54.646], [56.888, 58.524], [60.552, 62.875], [67.356, 70.256], [72.043, 74.391]], 
               [[1.612, 4.456], [7.171, 7.950], [16.976, 17.176], [26.234, 30.663], [31.857, 35.206], [36.357, 36.467], [64.871, 69.249], [74.441, 83.495]]
               ]
pu_channel = [0, 1, 2]

