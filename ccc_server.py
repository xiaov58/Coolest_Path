
# ccc_server.py
import socket
import select
import threading
import meta_data
import cPickle
from control_msg import *

class ccc_server(threading.Thread):
    def __init__(self, threadname, crn_manager):
        threading.Thread.__init__(self, name = threadname)
        self.crn_manager = crn_manager
        self.port = meta_data.server_port;
        self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.srvsock.bind( ("", meta_data.server_port) )
        self.srvsock.listen( meta_data.max_client )
        self.descriptors = [self.srvsock]
        print 'Control Server started on node %d' % (self.crn_manager.id)
        
    def run(self):
     while 1:
        # Await an event on a readable socket descriptor
        (sread, swrite, sexc) = select.select( self.descriptors, [], [])
    
        # Iterate through the tagged read descriptors
        for sock in sread:
    
          # Received a connect to the server (listening) socket
          if sock == self.srvsock:
            self.accept_new_connection()
          else:
            # Received something on a client socket
            str = sock.recv(meta_data.sock_buffer_size)
            if str == "":
                host,port = sock.getpeername()
                str = 'Client closed %s:%s' % (host, port)
                sock.close
                self.descriptors.remove(sock)
            else:
                ctrl_msg = cPickle.loads(str)
                # time sync signal
                if ctrl_msg.type == 1:
                    #ignore if time_sync_flag is already 1
                    if self.crn_manager.time_sync_flag == 0:
                        self.crn_manager.time_sync_con.acquire()
                        self.crn_manager.time_sync_flag = ctrl_msg.time_sync_flag
                        self.crn_manager.time_sync_con.notify() 
                        self.crn_manager.broadcast(str)
                        self.crn_manager.time_sync_con.release()
                        
                # channel utilazation info
                if ctrl_msg.type == 2:
                    print self.crn_manager.channel_utilization_table
                    print ctrl_msg.channel_utilization_table
                    #update link temprature table
                    for i in meta_data.neighbour_table[self.crn_manager.id]:
                        if i == ctrl_msg.sender_id:
                            self.crn_manager.neighbour_channel_mask[i] = ctrl_msg.channel_mask
                            for j in range(len(meta_data.channels)) :
                                self.crn_manager.link_temp_table[i][j] = 1 - (1-self.crn_manager.channel_utilization_table[j])*(1-ctrl_msg.channel_utilization_table[j])
                    print self.crn_manager.link_temp_table
                                
                # rts
                if ctrl_msg.type == 3:
                    print "receive RTS"
                    if self.crn_manager.status == 0:
                        
                        self.crn_manager.status = 2
                        print meta_data.channels[ctrl_msg.channel_id]
                        self.crn_manager.role.tb.set_freq(meta_data.channels[ctrl_msg.channel_id])
                        self.crn_manager.rx_con.acquire()
                        self.crn_manager.rx_con.notify()
                        self.crn_manager.rx_con.release()
                        rts_ack = rts_ack_msg(1)
                        rts_ack_string = cPickle.dumps(rts_ack)
                        self.crn_manager.socks_table[ctrl_msg.sender_id].send(rts_ack_string)
                    else: 
                        rts_ack = rts_ack_msg(0)
                        rts_ack_string = cPickle.dumps(rts_ack)
                        self.crn_manager.socks_table[ctrl_msg.sender_id].send(rts_ack_string)
            
                # rts ack
                if ctrl_msg.type == 4:
                    if ctrl_msg.ack == 1:
                        self.crn_manager.rts_ack_flag = 1
                        
                    self.crn_manager.rts_ack_con.acquire()
                    self.crn_manager.rts_ack_con.notify()
                    self.crn_manager.rts_ack_con.release()
                    
                # free
                if ctrl_msg.type == 5:                        
                    self.crn_manager.status = 0
                    self.crn_manager.tx_con.acquire()
                    self.crn_manager.tx_con.notify()
                    self.crn_manager.tx_con.release()
                        
                        # if multi node request new route, address only one is enough
    
    def accept_new_connection(self):
      newsock, (remhost, remport) = self.srvsock.accept()
      self.descriptors.append( newsock )
    
      newsock.send("Connected to ccc_server on node %d" % (self.crn_manager.id))
      str = "Client joined %s:%s" % (remhost, remport)
      print str
