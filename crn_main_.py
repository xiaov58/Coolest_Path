
# from system
import sys

# from gnuradio
from gnuradio import gr
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

# from current dir
import meta_data
from destination import destination
from source import source
from router import router
from receive_path import receive_path
from uhd_interface import uhd_receiver
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter



def preprocess():
    
    # enable realtime scheduling
    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: failed to enable realtime scheduling"
        
    # process parameters
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")
    expert_grp.add_option("-c", "--carrier-threshold", type="eng_float", default=30,
                      help="set carrier detect threshold (dB) [default=%default]")
    parser.add_option("-i","--id", default=0,
                      help="id: check out meta_data.py also.")
    
    receive_path.add_options(parser, expert_grp)
    uhd_receiver.add_options(parser)
    digital.ofdm_demod.add_options(parser, expert_grp)
    transmit_path.add_options(parser, expert_grp)
    digital.ofdm_mod.add_options(parser, expert_grp)
    uhd_transmitter.add_options(parser)

    (options, args) = parser.parse_args ()
    if int(options.id) == 0:
        sys.stderr.write("You must specify -i ID or --id ID\n")
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        options.rx_freq = meta_data.channels[1] * 1e9
        options.tx_freq = meta_data.channels[1] * 1e9
    
    return options

def main():

    options = preprocess()
    
    # assign diffrent job to diffrent role
    # source
    if meta_data.role_tup[int(options.id)] == 'source':
        
        # new object and build graph
        src = source(options)
        sb = src.tb
    
        sb.start()                      # start flow graph
        src.run()
        sb.wait()                       # wait for it to finish
    
    
    # router
    if meta_data.role_tup[int(options.id)] == 'router':
        
        # new object and build graph
        rout = router(options)
        rb = rout.tb
    
        rb.start()                      # start flow graph
        rout.run()
        rb.wait()                       # wait for it to finish
    
    # destination
    if meta_data.role_tup[int(options.id)] == 'destination':
        
        # new object and build graph
        dest = destination(options)
        db = dest.tb
    
        db.start()                      # start flow graph
        db.wait()                       # wait for it to finish
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
