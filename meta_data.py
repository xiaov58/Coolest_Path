
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.512, 2.511, 2.515, 2.513, 2.514]



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
pu_activity = [[], [[0.5207632382314826, 107.44762388523567]], [[9.306803125491207, 15.116091491023429], [22.263345330518646, 45.539949670391024], [56.47467283319621, 94.4636647225653]], [[4.935086136703185, 47.44481492451444], [77.60165339424901, 81.39786426047982]], [[32.844184581528424, 41.1918115756283], [42.84531625684578, 73.28272506891659]], [[35.62236625640508, 42.61364457767694], [56.07832801259456, 80.89638791241842]], [[28.842900072346513, 35.083646803624674], [36.23454390861041, 39.131630800574484], [41.45188562164844, 48.326635441672806], [69.69232886713836, 95.93274600333821]], [[9.321068420793209, 18.50176305851002], [29.835574051244137, 37.143624446154746], [47.756576934599835, 75.44464024656304]], [[1.6103298264935846, 6.162948470335427], [19.60611300437565, 22.43857751990107], [25.16363342983498, 68.19009007931606]], [[27.505200007876528, 97.18140734802799]], [[6.586814603998506, 52.244023556442336]]]
