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
	print('file server')
	print(request.remote[0])
	if not is_node_active(request.remote[0]):
		time.sleep(10)
	body = str(request.body,'utf-8')
	data = json.loads(body)
	if "file" in data and is_file_available(data["file"]):
		return OKResponse()
	if "download" in data and is_file_available(data["download"]):
		return FileResponse(Data.directory + data["download"])
	else:
		NotFound()

def sync_nodes(request):
	print("sync node")
	data = str(request.body,'utf-8')
	nodes = json.loads(data)

	for ip in nodes:
		if ip == "0.0.0.0":
			nodes[request.remote[0]] = {"ip":request.remote[0],"port":nodes[ip]["port"],"active":True}
			del nodes[ip]
			break
	update_nodes(nodes,lock_upload)
	return OKResponse()

@run_periodic
def discovery():
	print("start discovery")
	data = get_nodes()["nodes"]
	for ip in get_cluster():
		Request.post("sync:%s:%s/discovery"%(ip,UDP_PORT),data=json.dumps(data))

def request_file(node,file,lock):
	print('request file')
	print(node)
	res = Request.get("file:%s:%s/request/file"%(node["ip"],node["port"]),data=json.dumps({"file":file}))
	print(res.__dict__)
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
	print("node chosen")
	res = Request.get("file:%s:%s/request/file"%(node["ip"],node["port"]),data=json.dumps({"download":file}))
	if res.code == 123:
		print("download")
		f = open("application/files/%s"%(res.data['file_name']), 'w+b')
		f.write(res.data['binary'])
		f.close()
		active_node(node["ip"])
	else:
		print("file not found")


