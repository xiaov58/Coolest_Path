
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.512, 2.516, 2.515, 2.513, 2.514]



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
pu_activity = [[], [[4.890161168582374, 10.470354471001945], [13.476345462852784, 23.115877735892276], [38.154172632640694, 47.38197388364933], [87.17702029796766, 93.77836103871256]], [[9.688664515436294, 9.798031316004673], [11.023567337192, 30.105383026470946], [30.989887262931862, 66.32467945910793]], [[13.49645384685616, 21.214930585938966], [38.77261941871043, 41.61999341362261], [77.63499781737443, 102.40546778838309]], [[13.514596835430138, 17.854525165041156], [32.048157663168865, 55.430781903057365]], [[8.238294547827833, 9.773016841402278], [10.757145050026896, 36.17150477161859], [37.759326177648184, 50.32392869175786]], [[1.2367667729953515, 13.03342918606468], [38.306241094505594, 51.84120340215778]], [[17.90285497029607, 21.274337241633596], [38.36134422400959, 39.988348958164025], [48.802624034072124, 53.631787745876096]], [[12.004801529667194, 17.017571244179656], [18.64077509930212, 43.263591425683785], [66.58790726119483, 81.5826475617217]], [[35.866872821420415, 41.56922866767345], [59.131309030124406, 65.61634237356466]], [[3.982120884307077, 6.771024312402421], [26.762316773715998, 33.80541987730397], [71.47402528267085, 96.16199706347919]]]

