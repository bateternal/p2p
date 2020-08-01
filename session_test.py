from session import Session

from session.server import Server 

from session.client import Client

from threading import Thread

import sys

import time

session = Session.getInstance()

server = Server('127.0.0.1',65432)

server2 = Server('127.0.0.1',1113,socket_type='UDP')

t1 = Thread(target=server.start,args=())
t1.start()

t2 = Thread(target=server2.start,args=())
t2.start()

client = Client('127.0.0.1',65432,'TCP')

@session.handler_tcp
def message(socket_type, message , addr):
	print(message, addr,1)
	server.send(addr, b'1110')

@session.handler_udp
def message(socket_type, message , addr):
	print(message, addr)

client.send_tcp(b'hello TCP')

try:
	client.send_udp(b'hello UDP')
	print("fail")
except Exception as e:
	print(e)
	print("success")

client = Client('127.0.0.1',1113,'UDP')

client.send_udp(b'hello UDP')

time.sleep(2)
t1.join()
t2.join()
server.close()
server2.close()
sys.exit()
