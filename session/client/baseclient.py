
import socket, time

from settings import *

class BaseClient:

	def __init__(self, host, port, socket_type):
		if socket_type not in ["UDP","TCP"]:
			raise Exception("socket type must be tcp or udp")
		self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if socket_type == 'UDP' else socket.SOCK_STREAM) #socket.SOCK_STREAM socket.SOCK_DGRAM
		self.socket_type = socket_type
		self.check_point = 0
		self.host = host
		self.port = port
		if socket_type == "TCP":
			self.socket_object.settimeout(TIMEOUT)
			self.socket_object.connect((host, port))

	def __del__(self):
		try:
			self.socket_object.close()
		except:
			pass

	def request(self, data):
		if self.socket_type == "TCP":
			self.socket_object.sendall(data)
			data =  self.socket_object.recv(1024)
			return data

		else:
			self.socket_object.sendto(data, (self.host , self.port))
			return

	def close(self):
		try:
			self.socket_object.close()
		except:
			pass
							