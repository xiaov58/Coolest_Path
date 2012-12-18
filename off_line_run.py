
import meta_data
import cPickle
import sys
import os
import time
import socket
from off_line_server import off_line_server
from control_msg import *

id = 0
freq = 0
tx_id = 0
socks_table = {}

def broadcast(str):
    for k in socks_table.keys():
        socks_table[k].send(str)
    

def main():
    tx_id = int(sys.argv[2])
    freq = float(sys.argv[1])
    
    f = open("id", "r")
    for eachline in f:
        id = int(eachline)
    
#    # start ccc_server, recieve coming control msg only
#    off_line_server_ = off_line_server("off_line_server", id)
#    off_line_server_.setDaemon(True)
#    off_line_server_.start()
#    
#     #wait a while for setting up server on all nodes
#     #client sock is only used for sending msg out
#    time.sleep(meta_data.setup_time)
#    
#     #connet to server, use dict to store sock list
#     #key is the node id, value is the sock descriptor
#    for i in meta_data.neighbour_table[id]:
#        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#        sock.connect( (meta_data.ip_table[i], meta_data.server_port) )
#        print sock.recv( meta_data.sock_buffer_size )
#        socks_table[i] = sock

    if id == tx_id:
        time.sleep(1)
        os.system("python benchmark_tx.py -f "+ str(freq) +"G")
        print "DONE"
    else:
        os.system("python benchmark_rx.py -f "+ str(freq) +"G")
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
