
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
                        
                # sensing result
                if ctrl_msg.type == 2:
                    #update link temprature table
                    for i in meta_data.neighbour_table[self.crn_manager.id]:
                        if i == ctrl_msg.sender_id:
                            self.crn_manager.neighbour_channel_mask[i] = ctrl_msg.channel_mask
                            for j in range(len(meta_data.channels)) :
                                self.crn_manager.link_temp_table[i][j] = 1 - (1-self.crn_manager.channel_utilization_table[j])*(1-ctrl_msg.channel_utilization_table[j])
                                
                # rts
                if ctrl_msg.type == 3:
                    print "status : %d" % self.crn_manager.status
                    if self.crn_manager.status == 0:
                        self.crn_manager.status = 2
                        self.crn_manager.role.tb.set_freq(meta_data.channels[ctrl_msg.channel_id])                        
                        print "ready to receive at channel %d at %.3f" % (ctrl_msg.channel_id, self.crn_manager.get_virtual_time())
                        
                        rts_ack = rts_ack_msg()
                        rts_ack_string = cPickle.dumps(rts_ack)
                        self.crn_manager.socks_table[ctrl_msg.sender_id].send(rts_ack_string)
                    else:
                        self.crn_manager.rts_register_flag = 1
                        self.crn_manager.rts_register_id = ctrl_msg.sender_id
                        self.crn_manager.rts_register_channel = ctrl_msg.channel_id
                    #  reply later when buffer become empty
            
                # rts ack
                if ctrl_msg.type == 4:
                    self.crn_manager.rts_ack_con.acquire()
                    self.crn_manager.rts_ack_con.notify()
                    self.crn_manager.rts_ack_con.release()
                    
                # free over ccc
                if ctrl_msg.type == 5:              
                    print "get ccc free from % d at %.3f" % (ctrl_msg.sender_id, self.crn_manager.get_virtual_time())
                    self.crn_manager.status = 0

                # routing request
                if ctrl_msg.type == 6:    
                    if ctrl_msg.routing_request_cnt > self.crn_manager.routing_error_cnt:
                        # make up the task that need to be done when receive error msg, then block error msg
                        self.crn_manager.routing_error_cnt += 1
                        self.crn_manager.clear()
                            
                    self.crn_manager.get_best_links()
                    links = self.merge(ctrl_msg.links, self.crn_manager.best_links)
                    
                    if self.crn_manager.id != meta_data.destination_id:
                        ctrl_msg.path.append(self.crn_manager.id)

                        req = routing_request_msg(ctrl_msg.routing_request_cnt, ctrl_msg.path, links)
                        req_string = cPickle.dumps(req)
                        
                        for k in self.crn_manager.socks_table.keys():
                            if k not in ctrl_msg.path:
                                self.crn_manager.socks_table[k].send(req_string)
                    elif self.crn_manager.role.routing_request_cnt < ctrl_msg.routing_request_cnt:
                        self.crn_manager.role.links = self.merge(self.crn_manager.role.links, links)
                        if len(self.crn_manager.role.links) == self.crn_manager.role.link_number:
                            self.crn_manager.role.routing_request_cnt += 1
                            # run dijkstra
                            route = self.crn_manager.role.calculate_path()
                            print route
                           
                            #self.crn_manager.routing_reply_cnt += 1
                            rep = routing_reply_msg(self.crn_manager.routing_reply_cnt + 1, route)
                            rep_string = cPickle.dumps(rep)
                            self.crn_manager.broadcast(rep_string)
                                    
                # routing reply
                if ctrl_msg.type == 7:    
                    if self.crn_manager.routing_reply_cnt < ctrl_msg.routing_reply_cnt:
                        self.crn_manager.routing_reply_cnt += 1
                        self.crn_manager.route = ctrl_msg.route
                        print self.crn_manager.route
    
                        if ctrl_msg.route != [] and self.crn_manager.id in self.crn_manager.route:
                            if self.crn_manager.id != meta_data.destination_id:
                                print "try to wake from route error"
                                self.crn_manager.set_best_channel()
                                self.crn_manager.process_con.acquire()
                                self.crn_manager.process_flag = 1
                                self.crn_manager.process_con.notifyAll()
                                self.crn_manager.process_con.release()
                        self.crn_manager.broadcast(str)
            
                # error
                if ctrl_msg.type == 8:    
                    #ignore if already broadcasted error
                    if self.crn_manager.routing_error_cnt < ctrl_msg.routing_error_cnt:
                        self.crn_manager.routing_error_cnt += 1
                        self.crn_manager.clear()
                        
                        if self.crn_manager.id != meta_data.source_id:
                            self.crn_manager.broadcast(str)
                        else:
                            self.crn_manager.role.routing_request_cnt += 1
                            self.crn_manager.get_best_links()
                            path = [self.crn_manager.id]
                            req = routing_request_msg(self.crn_manager.role.routing_request_cnt, path, self.crn_manager.best_links)
                            req_string = cPickle.dumps(req)
                            self.crn_manager.broadcast(req_string)
                            
                # air_free reply
                if ctrl_msg.type == 9:              
                    print "fast wake up"
                    self.crn_manager.early_free_flag = 1
                    self.crn_manager.air_con.acquire()
                    self.crn_manager.air_con.notify()
                    self.crn_manager.air_con.release()

        
    def merge(self, a, b):
        c = []
        for i in a:
            if i not in b:
                c.append(i)
        for i in b:
            c.append(i)
            
        return c
    
    def accept_new_connection(self):
      newsock, (remhost, remport) = self.srvsock.accept()
      self.descriptors.append( newsock )
    
      newsock.send("Connected to ccc_server on node %d" % (self.crn_manager.id))
      str = "Client joined %s:%s" % (remhost, remport)
      print str
