
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
pu_id_table = [[] ,   []  ,   [1, 2, 3, 4, 5]  ,  [] , [] , [6, 7, 8, 9, 10] , []]
pu_channel = [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
pu_activity = [[], [[2.845440154394958, 6.797217707642172], [12.641308416344593, 50.653937857888934]], [[7.065023622731628, 13.848706406934351], [37.26035641010296, 37.39510767738323], [38.79628362083146, 81.92837250973534]], [[4.769795150555105, 6.098716410234437], [9.347353929341384, 24.212044872234692], [30.1996884168896, 38.79783965850372], [49.72461555348432, 56.42148792850062]], [[2.9171207619679875, 7.528118739308441], [8.04035750915791, 44.32234953896632], [48.49342555817704, 63.342849320803865]], [[2.4972508612562394, 6.932750329105959], [33.22693979084054, 37.08513379202115], [37.68354781997114, 39.70326100045731], [42.356206033552006, 43.59709909538807], [66.1320162551543, 70.28991624782834]], [[15.447708001025601, 16.51473009236921], [20.30764374171513, 20.88162504220537], [25.519807451507738, 63.266432837323386]], [[52.835537052583774, 54.17028255397552]], [[3.670368626525434, 6.208210578181486], [13.747183509170423, 19.28689025154869], [22.627564254619287, 67.71583549986528]], [[2.4793456246642585, 7.110696366143031], [21.268361860336007, 78.91852918965861]], [[4.322277434033371, 5.726819932618119], [16.389259915989765, 21.337989904018713], [35.56668767605497, 40.11628417508677], [47.32334903843017, 62.91311974595052]]]
