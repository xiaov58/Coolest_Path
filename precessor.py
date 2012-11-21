
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

def parse_parameters():
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")
    return parser
