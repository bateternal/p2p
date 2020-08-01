
class Session:

	def handler_udp(self, func):
		self.func_udp = func

	def handler_tcp(self, func):
		self.func_tcp = func

	def send_to_upper_layer(self, socket_type, message , addr):
		if socket_type == 0 and self.func_udp:
			self.func_udp(socket_type, message , addr)
		else socket_type == 1 and self.func_tcp:
			self.func_tcp(socket_type, message , addr)
