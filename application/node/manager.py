
from .data import Data

from presentation.view import FileServer, SyncServer

from .urls import *
from .utils import *
from .views import *

import logging


logging.basicConfig(filename="application/logs/p2p.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)



class Manager:

	@staticmethod
	def start():


		file_server = FileServer(host='0.0.0.0')
		sync_server = SyncServer(host='0.0.0.0')

		port1 = file_server.start()
		port2 = sync_server.start()
		with open(Data.node_config, 'w') as outfile:
			json.dump({"nodes":{"0.0.0.0":{"ip":"0.0.0.0","port":port1,"active":False}}},outfile)
		print("listening on 0.0.0.0:%s TCP"%port1)
		print("listening on 0.0.0.0:%s UDP"%port2)
		logging.info("listening on 0.0.0.0:%s TCP"%port1)
		logging.info("listening on 0.0.0.0:%s UDP"%port2)
		while True:
			print(">",end="")
			command = input()
			if "-l" in command:
				Data.cluster_list = command[command.index("-l")+1]
			if "-d" in command:
				Data.directory = command[command.index("-d")+1]
			if command == "list":
				print(get_cluster())

			elif len(command.split()) > 1 and command.split()[0] == "get":
				request_to_all(command.split()[1])

