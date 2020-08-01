
class Request:

	def __init__(self, url, remote, body, method ,subject):
		self.url = url
		self.remote = remote
		self.body = body
		self.method = method
		self.subject = subject