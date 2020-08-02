from presentation.view import View

from presentation.view import FileServer, SyncServer

from presentation.request import Request

import json, time

file_server = FileServer(host='127.0.0.1')
sync_server = SyncServer(host='127.0.0.1')

port1 = file_server.start()
port2 = sync_server.start()
print(port1,port2)
def test_1(request):
	print(request)
	print(request.__dict__)
	return "ok"

def test_2(request):
	print(request)
	print(request.__dict__)
	return "ok"

View.get("/request/file",test_1)
View.post("/sync",test_2)

Request.get("file:127.0.0.1:%s/request/file"%port1,data="")
Request.post("sync:127.0.0.1:%s/sync"%port2,data="")




def fileserver(request):
	body = str(request.body,'utf-8')
	data = json.loads(body)
	print(data)
	if "file" in data and data["file"] == "sample.txt":
		return "ok"
	if "download" in data:
		return "sample.txt"

View.get("/request/file",fileserver)


r = Request.get("file:127.0.0.1:%s/request/file"%port1,data=json.dumps({"file":"sample.txt"}))
if r:
	res = Request.get("file:127.0.0.1:%s/request/file"%port1,data=json.dumps({"download":"sample.txt"}))
	f = open("files/%s-%s"%(res['file_name'],str(time.time())), 'w+b')
	f.write(res['binary'])
	f.close()