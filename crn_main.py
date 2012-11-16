#!/usr/bin/env python
#
# Copyright 2006,2007,2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, blks2
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

from gnuradio import digital

# from current dir
from receive_path import receive_path
from uhd_interface import uhd_receiver
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter

import struct, sys, time, random

class my_top_block(gr.top_block):
    def __init__(self, callback, options):
        gr.top_block.__init__(self)

        if(options.rx_freq is not None):
            self.source = uhd_receiver(options.args,
                                       options.bandwidth,
                                       options.rx_freq, options.rx_gain,
                                       options.spec, options.antenna,
                                       options.verbose)

        if(options.tx_freq is not None):
            self.sink = uhd_transmitter(options.args,
                                        options.bandwidth,
                                        options.tx_freq, options.tx_gain,
                                        options.spec, options.antenna,
                                        options.verbose)

        # Set up receive path
        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the UHD sink)
        self.rxpath = receive_path(callback, options)
        self.txpath = transmit_path(options)

        self.connect(self.source, self.rxpath)
        self.connect(self.txpath, self.sink)
        

    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

def main():

    global n_rcvd, n_right, queue
        
    n_rcvd = 0
    n_right = 0
    queue = [] 

    def rx_callback(ok, payload):
        global n_rcvd, n_right
        n_rcvd += 1
        (pktno,src,dest,data) = struct.unpack('!H', payload[0:2], payload[2:4], payload[4:6], payload[6:])
        # reach destination
        if int(options.id) == 3:
            if ok:
                n_right += 1
            print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d \t src: %d \t dest: %d" % (ok, pktno, n_rcvd, n_right, src, dest)

        # retransmit
        if int(options.id) == 2:
            if ok:
                n_right += 1
            print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d \t src: %d \t dest: %d" % (ok, pktno, n_rcvd, n_right, src, dest)
            # save to queue
            payload_re = struct.pack('!H', pktno & 0xffff) + struct.pack('!H', 2 & 0xffff) + struct.pack('!H', 3 & 0xffff) + data
            queue.insert(0,payload_re)

        # overheard by 1
        if int(options.id) == 1:
            if ok:
                n_right += 1
            print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d \t src: %d \t dest: %d" % (ok, pktno, n_rcvd, n_right, src, dest)
    


    def send_pkt(payload='', eof=False):
        return tb.txpath.send_pkt(payload, eof)

    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")
    parser.add_option("-s", "--size", type="eng_float", default=400,
                      help="set packet size [default=%default]")
    parser.add_option("-M", "--megabytes", type="eng_float", default=1.0,
                      help="set megabytes to transmit [default=%default]")
    parser.add_option("-i","--id", default=0,
                      help="id: choose form 1 2 3")

    receive_path.add_options(parser, expert_grp)
    transmit_path.add_options(parser, expert_grp)
    digital.ofdm_mod.add_options(parser, expert_grp)
    digital.ofdm_demod.add_options(parser, expert_grp)
    uhd_transmitter.add_options(parser)
    uhd_receiver.add_options(parser)

    (options, args) = parser.parse_args ()

    if options.rx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.tx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.id == 0:
        sys.stderr.write("You must specify -i ID or --id ID\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    # build the graph
    tb = my_top_block(rx_callback, options)

    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:

        print "Warning: failed to enable realtime scheduling"

    tb.start()                      # start flow graph

    if int(options.id) == 1:
        # Source
        # generate and send packets
        nbytes = int(1e6 * options.megabytes)
        n = 0
        pktno = 0
        min_delay = 0.001
        pkt_size = int(options.size)

        while n < nbytes:
            data = (pkt_size - 6) * chr(pktno & 0xff) 
            payload = struct.pack('!H', pktno & 0xffff) + struct.pack('!H', 1 & 0xffff) + struct.pack('!H', 3 & 0xffff) + data

            # sense 
            time.sleep(10 * min_delay * random.random())
            delay = min_delay
            while tb.carrier_sensed():
                sys.stderr.write('B')
                time.sleep(delay)
                if delay < 0.05:
                    delay = delay * 2       # exponential back-off

            send_pkt(payload)
            n += len(payload)
            sys.stderr.write('.')
            pktno += 1
            
        send_pkt(eof=True)


    if int(options.id) == 2:
        # Router
        # if queue is not empty, try to send, compete with sender

        while len(queue) != 0:
            payload = queue.pop()

            # sense 
            time.sleep(10 * min_delay * random.random())
            delay = min_delay
            while tb.carrier_sensed():
                sys.stderr.write('B')
                time.sleep(delay)
                if delay < 0.05:
                    delay = delay * 2       # exponential back-off

            send_pkt(payload)
            n += len(payload)
            sys.stderr.write('.')
            pktno += 1
            
        send_pkt(eof=True)

    if int(options.id) == 3:
        # Destination
        pass

    tb.wait()                       # wait for it to finish

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
