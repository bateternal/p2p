from presentation.request import BaseClient

from session.client import Client

class FileClient(BaseClient):
	
	def __init__(self, *args, **kwargs):
		super(FileClient, self).__init__(*args, **kwargs)
		FileClient.client = Client(self.host,self.port,'TCP')

	def send_request(self, url, method, body):
		url = (url + ' '*20)[:20]
		method = (method + ' '*4)[:4]
		data = url.encode() + method.encode() + body.encode()
		response = FileClient.client.send_tcp(data)
		if response == b'1111':
			return True
		elif response:
			file_name = str(response[:20],'utf-8').replace(" ","")
			return {'file_name':file_name,'binary':response[20:]}
		

