
class Session:

	__instance = None

	@staticmethod 
	def getInstance():
		if Session.__instance == None:
			Session()
		return Session.__instance

	def __init__(self):
		if Session.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			Session.__instance = self

	def handler_udp(self, func):
		self.func_udp = func

	def handler_tcp(self, func=None):
		self.func_tcp = func

	def send_to_upper_layer(self, socket_type, message , addr):
		if socket_type == "UDP" and self.func_udp:
			self.func_udp(socket_type, message , addr)
		elif socket_type == "TCP" and self.func_tcp:
			self.func_tcp(socket_type, message , addr)
