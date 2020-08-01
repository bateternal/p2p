
import socket

class BaseClient:

	def __init__(self, host, port, socket_type):
		self.socket_object = socket.socket(socket.AF_INET, socket_type) #socket.SOCK_STREAM socket.SOCK_DGRAM
		self.socket_type = socket_type
		self.check_point = 0
		self.payload = b'0' if socket_type == 'UDP' else b'1'
		socket_object.connect((HOST, PORT))

	def __del__(self):
		try:
			self.socket_object.close()
		except:
			pass
			
	def request(self, data):
		data = self.payload + data
		socket_object.sendall(data)
		data =  socket_object.recv(1024)
		return data

	def close(self):
		try:
			self.socket_object.close()
		except:
			pass
							