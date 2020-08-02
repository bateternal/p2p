from presentation.view import View

from presentation.view import FileServer, SyncServer

from presentation.request import Request

from presentation.response import OKResponse, NotFound, FileResponse

import json, time

file_server = FileServer(host='127.0.0.1')
sync_server = SyncServer(host='127.0.0.1')

port1 = file_server.start()
port2 = sync_server.start()
print(port1,port2)
def test_1(request):

	print(request)
	print(request.__dict__)
	return OKResponse()

def test_2(request):
	print(request)
	print(request.__dict__)
	return OKResponse()

View.get("/request/file",test_1)
View.post("/sync",test_2)

Request.get("file:127.0.0.1:%s/request/file"%port1,data="")
Request.post("sync:127.0.0.1:%s/sync"%port2,data=json.dumps({"a":{"b":3},"c":"asdg"}))




def fileserver(request):
	body = str(request.body,'utf-8')
	data = json.loads(body)
	print(request.remote)
	print(data)
	if "file" in data and data["file"] == "sample.txt":
		return OKResponse("ok")
	if "download" in data:
		return FileResponse("sample.txt")

View.get("/request/file",fileserver)


r = Request.get("file:127.0.0.1:%s/request/file"%port1,data=json.dumps({"file":"sample.txt"}))
if r.code == 200:
	res = Request.get("file:127.0.0.1:%s/request/file"%port1,data=json.dumps({"download":"sample.txt"}))
	if res.code == 123:

		f = open("files/%s-%s"%(res.data['file_name'],str(time.time())), 'w+b')
		f.write(res.data['binary'])
		f.close()
	else:
		print("file not found")