#!/usr/bin/env python

import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 4675
BUFF_SIZE = 1024
MESSAGE = "THIS IS A TEST! PLEASE IGNORE!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFF_SIZE)
s.close()

print "received data:", data

