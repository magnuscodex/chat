#!/usr/bin/env python

import socket

TCP_IP = ""
TCP_PORT = 4675
BUFF_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection from:', addr
while True:
  data = conn.recv(BUFF_SIZE)
  if not data: break
  print "received data:", data
  conn.send(data)  # echo
conn.close()
