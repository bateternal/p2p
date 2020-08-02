from presentation.view import BaseServer
from presentation.view import View
from presentation.utils import Request
from presentation.utils import Port

from session.server import Server 
from session import Session

from threading import Thread

class SyncServer(BaseServer):
	session = Session.getInstance()

	def __init__(self, *args, **kwargs):
		super(SyncServer, self).__init__(*args, **kwargs)
		self.port = Port.get_free_udp_port()
		SyncServer.server = Server(self.host, self.port,socket_type='UDP')

	def start(self):
		t1 = Thread(target=self.server.start,args=())
		t1.start()
		return self.port


	@session.handler_udp
	def message(socket_type, message , addr):
		message = message.decode()
		url = message[:20].replace(" ","")
		method = message[20:24].replace(" ","")
		body = message[24:].encode()
		request = Request(url=url,method=method,remote=addr,
			body=body,subject="Sync")
		View.call_api(method,url,request)
