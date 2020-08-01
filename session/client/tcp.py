from session.client import BaseClient

class TCP(BaseClient):
	
	def send_tcp(self, data):
		if self.socket_type == 0:
			raise Exception("This connection is udp")
		data = self.request(data)
		packets = [None for i in range(10000)] #max size of file is 10MB or 10000 1KB
		while data != b'1111':
			header = data[:4]
			paylaod = data[4:]
			packets[int(header)] = str(paylaod,'utf-8')
			socket_object.sendall(b'1')
		packets.remove(None)
		data = "".join(packets)
		return data