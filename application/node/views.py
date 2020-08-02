from .decorators import *
from .utils import *
from .connection import Connection
from settings import *
from threading import Thread

from presentation.request import Request
from presentation.response import OKResponse, NotFound, FileResponse

lock_upload = threading.Lock()
lock_node = threading.Lock()

def file_server(request):
	if not is_node_active(request.remote["ip"]):
		time.sleep(10)
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
	update_nodes(nodes,lock_upload)
	return OKResponse()

@run_periodic
def discovery():
	data = get_nodes()["nodes"]
	for node in nodes.values():
		Request.post("sync:%s:%s/discovery"%(node["ip"],UDP_PORT),data=json.dumps(nodes))

def request_file(node,file,lock):
	res = Request.get("file:%s:%s/request/file"%(node["ip"],node["port"]),data=json.dumps({"file":file}))
	if res.code == 200:
		lock.acquire()
			choose_node_for_get_file(node,file)
		lock.release()

def request_to_all(file):
	Connection.reset()
	nodes = get_nodes()["nodes"].values()
	for node in nodes:
		Thread(target=request_file,args=(node,file,lock_node,)).start()

def choose_node_for_get_file(node,file):
	if Connection.target:
		return
	Connection.target = node
	res = Request.get("file:%s:%s/request/file"%(node["ip"],node["port"]),data=json.dumps({"download":file}))
	if res.code == 123:
		f = open("application/files/%s"%(res.data['file_name']), 'w+b')
		f.write(res.data['binary'])
		f.close()
		active_node(node["ip"])
	else:
		print("file not found")


