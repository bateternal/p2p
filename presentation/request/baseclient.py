
class BaseClient:

	def __init__(self,host,port,url,data):
		self.host = host
		self.port = port
		self.url = url
		self.data = data