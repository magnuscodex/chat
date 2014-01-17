#!/usr/bin/env python

import socket
import sys
import signal
from select import select

TCP_PORT = 4675
BUFF_SIZE = 1024
TIMEOUT = 1

def sig_handler(sig, frame):
  print "Exiting"
  #TODO make socket global and close it
  exit(0)

signal.signal(signal.SIGINT, sig_handler)

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
      if not data:
        s.close()
        exit(0)
      print data,
    else:
      received = False
      
s.close()


