from presentation.view import View

from presentation.utils import Request

class SyncServer(BaseServer):

	def __init__(self, *args, **kwargs):
		super(SyncServer, self).__init__(*args, **kwargs)
		port = Port.get_free_udp_port()
		SyncServer.server = Server(self.host, port)

	def start(self):
		t1 = Thread(target=self.server.start,args=())
		t1.start()

	@session.handler_udp
	def message(socket_type, message , addr):
		url = message[:20].replace(" ","")
		method = message[20:24].replace(" ","")
		body = message[24:]
		request = Request(url=url,method=method,remote=addr,
			body=body,subject="Sync")
		View.call_api(method,url,request)
