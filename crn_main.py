
# crn_main.py: parse arguments and establish sockets connections 

# from system
import sys
# from gnuradio
from gnuradio import gr
from gnuradio import digital
from gnuradio.eng_option import eng_option
from optparse import OptionParser
# from current dir
import meta_data
from receive_path import receive_path
from uhd_interface import uhd_receiver
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter
from crn_manager import crn_manager

def parse_args():
    # enable real time scheduling
    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: failed to enable real time scheduling"
        
    # parse parameters
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")
    expert_grp.add_option("-c", "--carrier_threshold", type="eng_float", default=meta_data.default_carrier_thredshold,
                      help="set carrier detect threshold (dB) [default=%default]")
    parser.add_option("-i","--id", default=meta_data.default_id,
                      help="id: check out meta_data.py also.")
    
    receive_path.add_options(parser, expert_grp)
    uhd_receiver.add_options(parser)
    digital.ofdm_demod.add_options(parser, expert_grp)
    transmit_path.add_options(parser, expert_grp)
    digital.ofdm_mod.add_options(parser, expert_grp)
    uhd_transmitter.add_options(parser)

    (options, args) = parser.parse_args ()
    if int(options.id) == meta_data.default_id:
        print int(options.id)
        sys.stderr.write("You must specify -i ID or --id ID\n")
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        options.rx_freq = meta_data.channels_freq_table[meta_data.init_channel_num] * 1e9
        options.tx_freq = meta_data.channels_freq_table[meta_data.init_channel_num] * 1e9
        options.bandwidth = (meta_data.default_bandwidth * 10000000.0)/4
    return options

def main():
    options = parse_args()
    my_crn_manager = crn_manager(options)
    
    # two threads: ccc_server and main schedule loop
    my_crn_manager.establish_ccc()
    my_crn_manager.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
