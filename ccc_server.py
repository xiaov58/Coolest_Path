
# ccc_server.py
import socket
import select
import time
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
        print "Control Server started on node %d" % (self.crn_manager.id)
    
    def accept_new_connection(self):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        newsock.send("Connected to ccc_server on node %d" % (self.crn_manager.id))
        print "Client joined %s:%s" % (remhost, remport)
        
    def run(self):
        while 1:
            # wait an event on a readable socket descriptor
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])
            # Iterate through the tagged read descriptors
            for sock in sread:
                # Received a connect to the server (listening) socket
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    # Received something on a client socket
                    recv_str = sock.recv(meta_data.sock_buffer_size)
                    if recv_str == "":
                        host,port = sock.getpeername()
                        print 'Client closed %s:%s' % (host, port)
                        sock.close
                        self.descriptors.remove(sock)
                    else:
                        ctrl_msg = cPickle.loads(recv_str)
                        
                        # time sync signal
                        if ctrl_msg.type == 1:
                            if self.crn_manager.time_sync_flag == False:
                                self.crn_manager.time_sync_con.acquire()
                                self.crn_manager.time_sync_flag = True
                                self.crn_manager.time_sync_con.notify() 
                                self.crn_manager.time_sync_con.release()
                                # spread this signal
                                self.crn_manager.broadcast(recv_str)
                            # ignore if time_sync_flag is already True
                            else:
                                pass
                        
                        # sensing_result_msg
                        if ctrl_msg.type == 2:
                            self.crn_manager.my_link_value_table.update_item(ctrl_msg.sender_id, 
                                                                          ctrl_msg.channel_util_table, 
                                                                          ctrl_msg.channel_mask_table,
                                                                          ctrl_msg.round_cnt)
                            if self.crn_manager.my_link_value_table.check_all_updated() == True:
                                print "OK"
                                
                            
                        
        
