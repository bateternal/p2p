from presentation.request import FileClient, SyncClient

class Request:

	@staticmethod
	def post(url,data):
		url_parts = url.split(":")
		protocol = url_parts[0]
		host = url_parts[1]
		port = url_parts[2].split("/")[0]
		url = ("+" + url_parts[2]).replace("+" + port,"")
		if protocol == "file":
			file_client = FileClient(host=host,port=port)
			return file_client.send_request(url,"POST",body=data)
		if protocol == "sync":
			sync_client = SyncClient(host=host,port=port)
			return sync_client.send_data(url,"POST",body=data)


	@staticmethod
	def get(url,data):
		url_parts = url.split(":")
		protocol = url_parts[0]
		host = url_parts[1]
		port = url_parts[2].split("/")[0]
		url = ("+" + url_parts[2]).replace("+" + port,"")
		if protocol == "file":
			file_client = FileClient(host=host,port=port)
			return file_client.send_request(url,"GET",body=data)
		if protocol == "sync":
			sync_client = SyncClient(host=host,port=port)
			return sync_client.send_data(url,"GET",body=data)