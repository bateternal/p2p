from .data import Data

from presentation.view import FileServer, SyncServer

class Manager:

	@staticmethod
	def start():
		raw_data = input().split()

		if "-l" in raw_data:
			Data.cluster_list = raw_data[raw_data.index("-l")+1]
		if "-d" in raw_data:
			Data.directory = raw_data[raw_data.index("-d")+1]


		file_server = FileServer(host='0.0.0.0')
		sync_server = SyncServer(host='0.0.0.0')

		port1 = file_server.start()
		port2 = sync_server.start()
		print("listening on 0.0.0.0:%s TCP"%port1)
		print("listening on 0.0.0.0:%s UDP"%port2)
		print(">",endswith="")