
import socket

class BaseClient:

	def __init__(self, host, port, socket_type):
		self.socket_object = socket.socket(socket.AF_INET, socket_type) #socket.SOCK_STREAM socket.SOCK_DGRAM
		self.socket_type = socket_type
		self.check_point = 0
		self.payload = b'0' if socket_type == 'UDP' else b'1'
		socket_object.connect((HOST, PORT))

	def __del__(self):
		self.socket_object.close()

	def request(self, data):
		data = self.payload + data
		socket_object.sendall(data)
		data =  socket_object.recv(1024)
		packets = [None for i in range(10000)] #max size of file is 10MB or 10000 1KB
		while data != b'1111':
			header = data[:4]
			paylaod = data[4:]
			packets[int(header)] = paylaod
				