
import socket

class BaseClient:

	def __init__(self, socket_type):
		self.socket_object = socket.socket(socket.AF_INET, socket_type) #socket.SOCK_STREAM socket.SOCK_DGRAM

	def __del__(self):
		self.socket_object.close()

	def request(self, host, port, data):
		s.connect((HOST, PORT))
		s.sendall(data)
		return s.recv(1024)