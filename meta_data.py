
# default option value
packet_size = 400           # Byte
carrier_thredshold = -60
bandwidth = 0.2       # MHz
channels = [0, 2.512, 2.516, 2.515, 2.513, 2.514]



# other experiment parameter
init_channel = 1
round = 50               
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
pu_activity = [
               [], 
               [[0.8870011862126667, 27.422999157158383], [37.036690523697544, 50.40180158038257], [53.22158988215553, 61.268139149816285], [67.21738770630276, 67.62133974878437], [70.25782908071578, 72.0536064699085], [80.45791909140058, 89.97243404492356], [102.75869730411685, 105.2931491405041], [113.71715241395638, 122.31011105726253], [133.71230449435933, 152.17220883152692], [156.50252725755888, 186.30897087305596]], 
               [[2.707650271651446, 9.92003776999282], [11.150510322981116, 13.370350624889815], [16.317068885341325, 18.54624200924109], [44.00119328780934, 66.81397735793682], [68.41288102247755, 70.84660576095355], [86.41457717040657, 90.96323377470708], [97.97196743342765, 98.76162956166486], [106.48038088897535, 120.86438238505237], [128.23067958635713, 128.6577330748025], [130.84583597886194, 138.39950050721734]], 
               [[14.734041537276704, 38.38054405397641], [44.754986311957204, 71.18581205156828], [75.13698504406943, 80.87394287017264], [86.88527151741471, 88.77960274113549], [89.90037476909649, 90.97028493579096], [101.40188702036785, 117.73389535780647], [130.73690853076346, 134.524741768551], [140.9054808287128, 142.81580680053716], [159.74642938532446, 160.91340396010696], [162.9174501118952, 179.135282595186]], 
               [[14.342547504464344, 31.44499039713976], [46.36229181979649, 48.30112740508065], [49.556848958388954, 51.509315975302954], [61.61622315511274, 74.82812649394947], [88.41191760053258, 89.01424857651497], [98.93149309998125, 100.37874173513494], [105.77194549131607, 122.30449829168347], [133.29796757268412, 136.6352642775087], [141.2945830118384, 150.81527250935102], [154.08657672585767, 159.2435123674437]], 
               [[4.678715684531156, 9.92230890158471], [15.961180638636922, 30.980935753441983], [33.49267103526697, 44.85703034799619], [62.23112304001135, 66.37665717088055], [77.36055876777601, 81.7781400118532], [97.07006818522001, 106.43520696857969], [138.32796835107308, 166.50155104683137], [200.6684366753439, 202.07680088077748], [209.11512527837826, 221.17043183278312], [227.1476934748396, 241.09997261927356]], 
               [[19.089282463657945, 25.007822403455403], [25.436386448914693, 26.528275243023142], [29.33724047213001, 36.382691539437744], [51.725308204741154, 66.02182654972485], [67.86474172379938, 76.25392210459256], [80.92635292306576, 81.91465339489035], [85.61118653672123, 96.59301846483106], [96.92298830239342, 112.39611923590762], [120.23261633244874, 122.29403996840249], [127.8764361215884, 141.75960451122543]], 
               [[7.9800711393189765, 10.937531494148889], [15.90674576839487, 19.558514177664552], [30.632483051550416, 40.93120830845963], [55.502034659939966, 58.08948649143501], [62.387077677952654, 64.43018210583001], [78.93873127810329, 110.35006579348044], [114.37745389962956, 134.2467100598433], [174.53986030039874, 180.25946734420555], [199.16890793608778, 225.78298574173513], [231.86706008635298, 239.8038346595379]], 
               [[0.404472531316186, 23.613944870322335], [29.233115737795032, 52.050631154230004], [60.31145428191975, 69.51571761253277], [76.47935166900145, 84.34190239976061], [86.00862058088747, 92.94150582923417], [98.27364382790181, 118.18295990463677], [123.56172483862011, 133.63463720081262], [145.92421883963556, 147.38049145637058], [151.8073859584993, 161.19445797482035], [170.89193728273546, 181.62085437854918]], 
               [[12.05549311108508, 15.240591959563298], [15.732972533996094, 32.05638210112367], [42.095651455695844, 46.627788109522754], [51.6892061736959, 86.84934447628459], [126.86454291903661, 137.96633047210088], [141.11100598507696, 174.9429315273691], [188.6679556005549, 192.6437135679289], [200.15574421545432, 207.46812639376338], [214.00018269581815, 217.24803109252454], [221.54140300087283, 228.72466212935115]], 
               [[9.498145593999809, 13.351309954863492], [22.6733587827464, 31.747394863294126], [54.19713801533338, 58.34554915564504], [64.3604202019431, 64.72763965328375], [70.77221569910822, 80.99489650408094], [84.98645695855734, 95.95389123171518], [109.850922020498, 111.91742870237519], [146.61271467802192, 185.3899893734206], [188.47890331488756, 199.61938504345432], [213.9640027875854, 218.51256797745697]]
               ]


