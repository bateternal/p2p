from presentation.request import BaseClient

from presentation.response import OKResponse, NotFound, FileResponse

from session.client import Client

class SyncClient(BaseClient):
	
	def __init__(self, *args, **kwargs):
		super(SyncClient, self).__init__(*args, **kwargs)
		SyncClient.client = Client(self.host,self.port,'UDP')

	def send_data(self, url, method, body):
		url = (url + ' '*20)[:20]
		method = (method + ' '*4)[:4]
		data = url.encode() + method.encode() + body.encode()
		response = SyncClient.client.send_udp(data)
		return OKResponse()