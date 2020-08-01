from session.client import BaseClient

class UDP(BaseClient):
	
	def send_udp(self, data):
		if self.socket_type == 1:
			raise Exception("This connection is tcp")
		self.request(data)
		self.close()