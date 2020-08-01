
class Port:

	@staticmethod
	def get_free_tcp_port():
		tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp.bind(('', 0))
		addr, port = tcp.getsockname()
		tcp.close()
		return port

	@staticmethod
	def get_free_udp_port():
		tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		tcp.bind(('', 0))
		addr, port = tcp.getsockname()
		tcp.close()
		return port

