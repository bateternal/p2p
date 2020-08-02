from presentation.view import BaseServer
from presentation.view import View
from presentation.utils import Request
from presentation.utils import Port
from presentation.response import OKResponse, NotFound, FileResponse

from session.server import Server
from session import Session

from threading import Thread

class FileServer(BaseServer):
	session = Session.getInstance()

	def __init__(self, *args, **kwargs):
		super(FileServer, self).__init__(*args, **kwargs)
		self.port = Port.get_free_tcp_port()
		FileServer.server = Server(self.host, self.port)

	def start(self):
		t1 = Thread(target=self.server.start,args=())
		t1.start()
		return self.port

	@session.handler_tcp
	def message(socket_type, message , addr):
		message = message.decode()
		url = message[:20].replace(" ","")
		method = message[20:24].replace(" ","")
		body = message[24:].encode()
		request = Request(url=url,method=method,remote=addr,
			body=body,subject="File")
		response = View.call_api(method,url,request)
		if response.code == 200:
			FileServer.server.send_ack(addr, True)
		elif response.code == 404:
			FileServer.server.send_ack(addr)
		elif response.code == 123:
			data = response.data
			file_data = open(data,'rb').read()
			file_data = (response.data + ' '*20)[:20].encode() + file_data
			FileServer.server.send(addr,file_data)

	@staticmethod
	def send(addr, message):
		FileServer.server.send(addr, message)

