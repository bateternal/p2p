from .decorators import *
from .utils import *

from threading import Thread

from presentation.request import Request
from presentation.response import OKResponse, NotFound, FileResponse

def file_server(request):
	body = str(request.body,'utf-8')
	data = json.loads(body)
	if "file" in data and is_file_available(data["file"]):
		return OKResponse()
	if "download" in data and is_file_available(data["download"]):
		return FileResponse(data["download"])
	else:
		NotFound()

def sync_nodes(request):
	data = str(request.body,'utf-8')
	nodes = json.loads(data)
	nodes.append({"ip":request.remote[0],"port":request.remote[1]})
	update_nodes(nodes)
	return OKResponse()

@run_periodic
def discovery():
	nodes = get_nodes()
	data = nodes
	for node in nodes:
		Request.post("sync:%s:%s/discovery"%(node["ip"],node["port"]),data=json.dumps(nodes))

def request_file(node,file):
	res = Request.get("file:%s:%s/request/file"%(node["ip"],node["port"]),data=json.dumps({"file":file}))

def request_to_all(file):
	nodes = get_nodes()
	for node in nodes:
		Thread(target=request_file,args=(node,file,)).start()

def choose_node_for_get_file(node):
	pass


