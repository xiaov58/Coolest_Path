
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
pu_activity = [[], [[31.358765557170518, 34.626720601745205], [44.426699590273046, 49.914595068927], [72.08837675322005, 73.04536180602422]], [[8.940857944108936, 23.69124192243349], [27.86792087186671, 32.689619017766795], [39.98884293358093, 56.68046648051968]], [[4.927374422750286, 5.659457368061971], [27.900591164877703, 32.95646672794308], [43.205250019250364, 57.202747630756726]], [[5.600860923490061, 12.634319503989838], [16.976131088500185, 40.329110506749], [44.1892008255409, 48.74831321502121], [49.01094107116165, 51.97565930188395]], [[1.8169329687923848, 25.38192316568497], [25.434882882334428, 26.058862842094896], [29.02702558872418, 29.422726809881446], [33.715862493035694, 34.03860297801901], [36.67474942275972, 38.41066760771788], [40.054486181307894, 99.67694754518295]], [[7.2283873597086785, 11.7007730810761], [11.840867256350617, 12.718687414013726], [12.965519347897773, 37.26482449335506], [46.147868352232315, 53.456802115541]], [[10.605203393690125, 11.790554295391557], [21.29717018443688, 22.96444699362435], [83.1081554720588, 86.44506695213902]], [[9.499852167324997, 18.178547049185845], [31.271418632364526, 32.684196690543835], [38.575138559360575, 41.08806748988244], [48.565222112801834, 53.1598974176962]], [[1.3546048022083557, 9.686651499584961], [12.207711032464761, 14.638071711813087], [26.73605344866794, 33.754151213544986], [38.894463444380676, 64.20496882593858]], [[4.779407029710993, 31.79018594271861], [77.74428126462999, 81.25586029459808]]]
