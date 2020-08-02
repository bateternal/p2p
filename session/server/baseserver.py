from session import Session

import socket
from threading import Thread

class BaseServer:

	__clients = {}

	while_condition = True

	def __init__(self, host ,port ,socket_type='TCP'):
		self.socket_type = socket_type
		if socket_type == 'UDP':
			self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket_object.bind((host, port))
		else:
			self.socket_object = socket.socket()
			self.socket_object.bind((host, port))
			self.socket_object.listen(5) 

	def start(self):
		if self.socket_type == "TCP":
			while True:
				clientsocket, addr = self.socket_object.accept()
				self.__clients[addr] = clientsocket
				self.start_new_thread(self.on_new_client,(clientsocket,addr))
		else:
			self.on_new_udp_client()


	def start_new_thread(self ,target ,args):
		t = Thread(target=target,args=args)
		t.start()

	def on_new_udp_client(self):
		while True:
			data, address = self.socket_object.recvfrom(4096)
			if data and data != b'':
				Session.getInstance().send_to_upper_layer(self.socket_type ,data ,address)
				# sent = self.socket_object.sendto(data, address)

	def on_new_client(self, clientsocket, addr):
		while True:
			msg = clientsocket.recv(1024)
			if msg and msg != b'':
				Session.getInstance().send_to_upper_layer(self.socket_type ,msg ,addr)
			
	def close(self):
		for addr in self.__clients:
			self.__clients[addr].close()

	def send_ack(self, addr ,payload=False):
		clientsocket = self.__clients[addr]
		response = b'1111' if payload else b'1000'
		clientsocket.send(response)

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