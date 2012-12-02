# Options value
source_id = 1
destination_id = 3
packet_size = 400           # Byte
total_size = 1                  # Mega Byte
default_carrier_thredshold = -50
min_delay = 0.001          # unit: second
random_backoff_range = 100 #ms
server_setup_time = 5
client_setup_time = 100
server_port = 11012
max_client = 5
sock_buffer_size = 100

channels = (0, 4.915, 4.917, 4.919)

# Topology
# first item is null to make it easy to count
role_tup =                    (''      , 'source'                 , 'router'                 , 'destination'      ) 
neightbour_tup =         ([]      ,   [2]                          ,   [1, 3]                      , [2]                          ) 
ip_tup =                       (''      , '128.205.39.104'  , '67.20.207.30'  , '128.205.39.100') 
neightbour_tup =         ([]      ,   []                            ,   [1]                          , [2]                          ) 

#Options:
#  -h, --help            show this help message and exit
#  -s SIZE, --size=SIZE  set packet size [default=400]
#  -M MEGABYTES, --megabytes=MEGABYTES
#                        set megabytes to transmit [default=1.0]
#  --discontinuous       enable discontinuous mode
#  --from-file=FROM_FILE
#                        use intput file for packet contents
#  --to-file=TO_FILE     Output file for modulated samples
#  --tx-amplitude=AMPL   set transmitter digital amplitude: 0 <= AMPL < 1.0
#                        [default=0.1]
#  -W BANDWIDTH, --bandwidth=BANDWIDTH
#                        set symbol bandwidth [default=500000.0]
#  -m MODULATION, --modulation=MODULATION
#                        set modulation type (bpsk, qpsk, 8psk, qam{16,64})
#                        [default=bpsk]
#  -f FREQ, --freq=FREQ  set Tx and/or Rx frequency to FREQ [default=none]
#  -a ARGS, --args=ARGS  UHD device address args [default=]
#  --spec=SPEC           Subdevice of UHD device where appropriate
#  -A ANTENNA, --antenna=ANTENNA
#                        select Rx Antenna where appropriate
#  --tx-freq=FREQ        set transmit frequency to FREQ [default=none]
#  --tx-gain=TX_GAIN     set transmit gain in dB (default is midpoint)
#  -v, --verbose         
#
#  Expert:
#    --log               Log all parts of flow graph to file (CAUTION: lots of
#                        data)
#    --fft-length=FFT_LENGTH
#                        set the number of FFT bins [default=512]
#    --occupied-tones=OCCUPIED_TONES
#                        set the number of occupied FFT bins [default=200]
#    --cp-length=CP_LENGTH
#                        set the number of bits in the cyclic prefix
#                        [default=128]
