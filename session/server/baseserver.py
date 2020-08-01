from session import Session

import socket
from threading import Thread

class BaseServer:

	__clients = {}

	def __init__(self, host ,port):
		self.socket_object = socket.socket()
		self.socket_object.bind((host, port))
		self.socket_object.listen(5) 

	def start(self):
		while True:
			clientsocket, addr = socket_object.accept()
			self.__clients[addr] = clientsocket
			start_new_thread(on_new_client,(clientsocket,addr))

	def start_new_thread(self ,target ,args):
		t = Thread(target=target,args=args)
		t.daemon = True
		t.start()

	def on_new_client(clientsocket, addr):
		while True:
			#TODO
			msg = clientsocket.recv(1024)
			socket_type = msg[:1]
			if socket_type == b'0':
				#TODO udp
				Session.send_to_upper_layer(int(socket_type) ,msg[1:] ,addr)
				clientsocket.close()
				del self.__clients[addr]
			else:
				Session.send_to_upper_layer(int(socket_type) ,msg[1:] ,addr)
			
	def close(self, addr):
		self.__clients[addr].close()
		del self.__clients[addr]

	def send(self, addr ,data):
		clientsocket = self.__clients[addr]
		response = b'0000'
		clientsocket.send(response)
		check_point = 0
		while True:
			msg = clientsocket.recv(1024)
			if msg != b'1':
				continue
			if check_point*1000 > len(data):
				response = b'1111'
				clientsocket.send(response)
				break

			target = data[check_point*1000:check_point*1000+1000]
			header = str(10000 + check_point + 1)[1:].encode()
			response = header + target
			clientsocket.send(response)
			check_point += 1
				



