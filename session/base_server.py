
import socket
from threading import Thread

class BaseServer:

	def __init__(self, host ,port):
		self.socket_object = socket.socket()
		self.socket_object.bind((host, port))
		self.socket_object.listen(5) 

	def start(self):
		while True:
			clientsocket, addr = socket_object.accept()
			start_new_thread(on_new_client,(clientsocket,addr))

	def start_new_thread(self ,target ,args):
		t = Thread(target=target,args=args)
		t.daemon = True
		t.start()

	def on_new_client(clientsocket ,addr):
		while True:
			#TODO
			msg = clientsocket.recv(1024)
			print(addr, ' >> ', msg)
			clientsocket.send(b'agsdfhdt')
		clientsocket.close()
