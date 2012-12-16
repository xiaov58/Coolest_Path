
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.512, 2.511, 2.510, 2.513, 2.514]



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
pu_activity =[[], [[1.4132844327003127, 3.617555631831822], [6.532369174448366, 9.031175518074203], [19.519704723905, 19.588020527556534], [21.30726599050552, 22.39395966470133], [29.522643750645745, 34.00302659335482], [40.25450376026799, 42.33793790268269], [51.91972054239918, 53.750907365797644]], [[6.885157098566067, 7.264467614047951], [8.354250692937764, 8.697423697405359], [12.61743564005129, 12.847838943389183], [21.39145691995757, 26.25473053440823], [26.382052909403715, 27.516037962133257], [27.842982927884393, 28.338112845811892], [37.56358238834996, 37.60404024630685], [52.94338640232057, 57.804756528843136]], [[3.649781055875541, 4.506537922908156], [27.31707555390819, 35.6733697648619], [39.26897780841753, 47.281005597020965], [64.65478460798812, 65.37088340710224]], [[4.47163933197402, 4.75005891375258], [41.22045787814652, 41.75859053322053], [50.230642737652175, 53.207750817487714]], [[4.1473868435381505, 5.098817744579327], [8.079018346276577, 8.96715629467652], [17.605704775251887, 19.57277587055265], [41.55660170071038, 42.15874450395941], [42.282754431985126, 42.49808115206864], [70.66359276737953, 70.82947430466992]], [[18.674186552725534, 21.475090684353287], [38.298367018425196, 38.40569576019444], [40.360657472696026, 40.78074274891417], [42.634263533040624, 43.49537612055908], [50.64113353347312, 51.74562080163668]], [[4.923779813271177, 8.033831486689909], [11.355028207316527, 11.554691732618044], [18.63698370720772, 20.957435739888375], [44.83256582209469, 47.77867985704118], [62.62692833703497, 67.47138310462707]], [[26.833375227061097, 27.388394339555774], [43.55845651207531, 45.38661192811292], [53.93714190596279, 56.803805771317336]], [[0.37486401255618595, 2.1407927681573735], [17.015404071502115, 17.96685175719371], [52.626107449749995, 53.15037272637111]], [[29.596432261289795, 30.161265574404307], [36.4806362932115, 43.36886010541202], [51.574661605444085, 53.51804427332916]]]
