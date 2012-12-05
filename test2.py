import time,sched

def event_func(msg):
    a = time.time()
    print "Current Time:%10.3f" % a

if __name__ == "__main__":

    s = sched.scheduler(time.time,time.sleep)

    s.enter(1,2,event_func,("Small event.",))
    s.enter(2,1,event_func,("Big event.",))
    s.run()
    while True:
        time.sleep(100)
