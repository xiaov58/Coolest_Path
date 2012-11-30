import time
from threading import Timer
def print_time():
    timer = Timer(2, print_time, ())
    timer.setDaemon(True)
    timer.start()
    print "From print_time", time.time()

def main():
    print time.time()
    timer = Timer(2, print_time, ())
    timer.setDaemon(True)
    timer.start()
    while 1:
        a = 0
        a = a +1
    #time.sleep(11)  # sleep while time-delay events execute
    print time.time()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
