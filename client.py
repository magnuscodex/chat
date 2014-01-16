#!/usr/bin/env python

import socket
import sys
from select import select

TCP_PORT = 4675
BUFF_SIZE = 1024
TIMEOUT = 1

host = raw_input("server name:")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, TCP_PORT))
while True:
  rlist, _, _ = select([sys.stdin], [], [], TIMEOUT)
  if rlist:
    msg = sys.stdin.readline()
    s.send(msg)
  received = True
  while received:
    rlist, _, _ = select([s], [], [], TIMEOUT)
    if rlist:
      data = s.recv(BUFF_SIZE)
      print data,
    else:
      received = False
      
s.close()


