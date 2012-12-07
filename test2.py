import thread, time , sys

def main():
    i = 1
    while 1:
        print "B"
        time.sleep(0.1)
        i += 1
        if i == 5:
            thread.start_new_thread(interrupt, ())  
    
def interrupt():
    print "try to interrupt"
    thread.interrupt_main()

try:  
    main()
except KeyboardInterrupt:  
    print 'error'
print 'over'  
