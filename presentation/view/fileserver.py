from presentation.view import View

from presentation.utils import Request

class FileServer(BaseServer):

	def __init__(self, *args, **kwargs):
		super(FileServer, self).__init__(*args, **kwargs)
		port = Port.get_free_tcp_port()
		FileServer.server = Server(self.host, port)

	def start(self):
		t1 = Thread(target=self.server.start,args=())
		t1.start()

	@session.handler_tcp
	def message(socket_type, message , addr):
		url = message[:20].replace(" ","")
		method = message[20:24].replace(" ","")
		body = message[24:]
		request = Request(url=url,method=method,remote=addr,
			body=body,subject="File")
		response = View.call_api(method,url,request)
		if response == "ok":
			FileServer.server.send_ack(addr, True)
		elif response == "nok":
			return
		else:
			#TODO‌conevrt file to binary
			FileServer.server.send(addr,response.encode())

	@staticmethod
	def send(addr, message):
		FileServer.server.send(addr, message)

