#!/usr/bin/env python

import socket
import threading
import atexit
import signal
import os
import time
from select import select

TCP_IP = ""
TCP_PORT = 4675
BUFF_SIZE = 1024
TIMEOUT = 1

#Make ^c exit whole process and not just main thread
def sig_handler(sig, frame):
  print "Exiting"
  #TODO make socket global and close it
  os._exit(0)
signal.signal(signal.SIGINT, sig_handler)

def on_exit(conns):
  for c in conns:
    if c: c.close()

connections = []

#Function to be run in separate thread
def connect_clients(sock, lock):
  while True:
    conn, addr = sock.accept()
    print "Connection from:", addr
    lock.acquire()
    connections.append(conn)
    lock.release()

#Bind listening socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

atexit.register(on_exit, connections)

#Bind initial client connection
conn, addr = s.accept()
print 'Connection from:', addr
connections.append(conn)

#Spin off thread to listen for new clients
m_conns = threading.Lock()  #Lock for the connections variable
client_listener = threading.Thread(target=connect_clients, args=(s, m_conns))
client_listener.start()

#Main loop to receive message and send them to all clients other
# than the sending client.
while len(connections) > 0:
  print len(connections)
  received = []
  m_conns.acquire()
  #Listen to all connections in turn.
  #TODO: Update so that select waits on connections simultaneously
  for i in range(0, len(connections)):
    conn = connections[i]
    rlist, _, _ = select([conn], [], [], TIMEOUT)
    if rlist:  
      data = conn.recv(BUFF_SIZE)
      received += [data]
      if data:
        print "received: ", data
      else:
        connections[i].close()
        connections[i] = None
    else:
      #The received list needs a 1-1 correspondence with the connections list
      #This is used to pair messages with sending clients
      received += [None]
  #Send messages received to all but sending client.
  for i in range(0, len(received)):
    msg = received[i]
    if not msg:
      continue
    for k in range(0, len(connections)):
      if i != k and connections[k] != None:
        connections[k].send(msg)
  connections = filter(None, connections)
  m_conns.release()
  time.sleep(1) #Appears to be required to all other thread to acquire lock
s.close()
os._exit(0)
