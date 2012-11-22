
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
        self.source = uhd_receiver(options.args,
                                       options.bandwidth,
                                       options.rx_freq, options.rx_gain,
                                       options.spec, options.antenna,
                                       options.verbose)

        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the UHD sink)
        self.txpath = transmit_path(options)
        self.connect(self.txpath, self.sink)
        self.rxpath = receive_path(callback, options)
        self.connect(self.source, self.rxpath)
        
    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()
