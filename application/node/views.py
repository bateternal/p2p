from .decorators import *
from .utils import *

from settings import *

from presentation.response import OKResponse, NotFound, FileResponse

lock_upload = threading.Lock()


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




