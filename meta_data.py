
# default option value
default_id = 100       #Magic number
default_packet_size = 400           # Byte
default_carrier_thredshold = -60
default_bandwidth = 0.2       # MHz

# channel info
init_channel_num = 0
channels_freq_table = [2.5120, 2.5125, 2.513, 2.5135, 2.514]

# time
ccc_server_setup_time = 1               # second
connection_setup_time = 1               # second
time_sync_setup_time = 1                # second


round = 25               

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
source_id = 0
destination_id = 5
full_duplex_mask =       [0, 1, 0, 1, 0, 1]
neighbour_table =        [[1, 3], [0, 2, 4] , [1, 3, 5] , [0, 2, 4] , [1, 3, 5] , [2, 4]] 
ip_table =               ['11.0.0.10', '11.0.0.11', '11.0.0.12', '11.0.0.13', '11.0.0.14', '11.0.0.15'] 


# PU info (first item is null to make it easy to count)
pu_id_table = [[] ,   []  ,   [1, 2, 3, 4, 5]  ,  [] , [] , [6, 7, 8, 9, 10] , []]
pu_channel = [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
pu_activity = [[], [[0.5276835060833122, 1.7574079373979132], [6.934452345326319, 10.704694333136578], [42.507367428078446, 43.26597225280358], [68.47278923745881, 71.84520872866993]], [[13.805154497510784, 14.552480668638697], [19.451740573495965, 27.255008249123513], [38.18175300579293, 39.405954905169196], [44.350043512149654, 46.95021256621646], [47.98151717838743, 51.81389139046885]], [[3.3580035392947996, 7.322978413205663], [9.829116049134774, 9.918560093594632], [20.440841068920903, 21.147395278703875], [29.82222981499538, 36.653975033069045], [39.60986088867095, 40.43103979713462], [48.190847059425025, 49.254196123997396], [63.713447166492095, 64.06963166640737]], [[4.738587271990584, 5.128515481898994], [20.073466038866176, 22.341244259188382], [23.182076434511604, 25.814683453862912], [25.89108498290569, 26.297781804600213], [27.771190581018303, 27.928391475036808], [32.72393597474377, 35.95945850389834], [40.43920292447255, 43.5143627727757], [46.96206855426337, 56.007114073756235]], [[10.699446369035039, 11.129429106917698], [14.664325637188583, 15.22373144151226], [15.847725111217233, 21.842136351222376], [31.41866034977323, 32.57330013152703], [44.35262515736573, 44.95136035175318], [51.62965357799838, 54.71887066553108]], [[12.791047317871659, 13.608418537361645], [14.863435799178657, 16.157933487283007], [17.680038582389404, 18.64601983042647], [22.724071342643406, 24.132693755917778], [32.62207433642763, 37.083592637734085], [71.63907298292008, 73.14417106786566]], [[7.410370133563516, 8.087725354152823], [21.56200268078537, 39.28681169854573], [40.37919216317205, 51.45947597965366]], [[6.59340740849073, 6.952798206825356], [52.898135191928915, 54.39889283593693]], [[6.63298418821146, 8.485852904154978], [13.978711491618032, 17.49078550872095], [24.666516160126285, 24.753552606641527], [49.17390761247128, 49.30172039583718], [60.63195727806733, 62.10652644706677]], [[5.369940095420518, 6.729187406095762], [7.283131516622867, 13.810286255007657], [31.592699094470902, 32.6069642228714], [34.279063166447756, 34.56868807298099], [36.920429759564264, 38.85829590309634], [48.80414266662821, 49.07038869653849], [66.30816376838874, 67.62172105709149]]]
