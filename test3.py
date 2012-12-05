import cPickle
from control_msg import *


cum = channel_utilazation_msg(2, 1, [0, 0, 0, 0.5])
cum_string = cPickle.dumps(cum)

str = cum_string

ctrl_msg = cPickle.loads(str)
print ctrl_msg.type
print ctrl_msg.sender_id
print ctrl_msg.cut
