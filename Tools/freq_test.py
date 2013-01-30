
#usage example: python freq_test.py 2.512 0

import sys
import os
import time

node_id = 0
freq = 0
tx_id = 0
socks_table = {}

def main():
    freq = float(sys.argv[1])
    tx_id = int(sys.argv[2])
    
    f = open("id", "r")
    for eachline in f:
        node_id = int(eachline)

    if node_id == tx_id:
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
