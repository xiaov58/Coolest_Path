
# from system
import sys

# from gnuradio
from gnuradio import gr

# from current dir
from receive_path import receive_path
from uhd_interface import uhd_receiver

class destination_block(gr.top_block):
    def __init__(self, callback, options):
        gr.top_block.__init__(self)

        self.source = uhd_receiver(options.args,
                                       options.bandwidth,
                                       options.rx_freq, options.rx_gain,
                                       options.spec, options.antenna,
                                       options.verbose)

        # Set up receive path
        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the UHD sink)
        self.rxpath = receive_path(callback, options)
        self.connect(self.source, self.rxpath)
