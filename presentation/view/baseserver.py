from session import Session

class BaseServer:

	def __init__(self, host):
		self.host = host
		self.session = Session.getInstance()