import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(("128.205.39.100",11012))
client_sock.send("Hello,server!")
print client_sock.recv(100)
client_sock.close()
