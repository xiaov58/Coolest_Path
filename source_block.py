
# from system
import sys

# from gnuradio
from gnuradio import gr

# from current dir
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter

class source_block(gr.top_block):
    def __init__(self, options):
        gr.top_block.__init__(self)

        self.sink = uhd_transmitter(options.args,
                                        options.bandwidth,
                                        options.tx_freq, options.tx_gain,
                                        options.spec, options.antenna,
                                        options.verbose)

        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the UHD sink)
        self.txpath = transmit_path(options)
        self.connect(self.txpath, self.sink)
