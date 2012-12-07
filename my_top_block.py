
# from system
import sys

# from gnuradio
from gnuradio import gr, digital

# from current dir
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter
from receive_path import receive_path
from uhd_interface import uhd_receiver

class my_top_block(gr.top_block):
    def __init__(self, callback, options):
        gr.top_block.__init__(self)

        self.source = uhd_receiver(options.args,
                                   options.bandwidth,
                                   options.rx_freq, options.rx_gain,
                                   options.spec, options.antenna,
                                   options.verbose)

        self.sink = uhd_transmitter(options.args,
                                    options.bandwidth,
                                    options.tx_freq, options.tx_gain,
                                    options.spec, options.antenna,
                                    options.verbose)

        self.txpath = transmit_path(options)
        self.rxpath = receive_path(callback, options)

        self.connect(self.txpath, self.sink)
        self.connect(self.source, self.rxpath)

    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()

    def set_freq(self, target_freq):
        """
        Set the center frequency we're interested in.
        """
        self.set_snk_freq(target_freq)
        self.set_src_freq(target_freq)
#        self.u_snk.set_freq(target_freq)
#        self.u_src.set_freq(target_freq)

