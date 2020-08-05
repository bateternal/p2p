from .decorators import *
from .utils import *

from settings import *

from presentation.response import OKResponse, NotFound, FileResponse

lock_upload = threading.Lock()


def file_server(request):
	print('\nfile server',request.remote[0],"\n>",end='')
	if not is_node_active(request.remote[0]):
		time.sleep(10)
	body = str(request.body,'utf-8')
	data = json.loads(body)
	if "file" in data and is_file_available(data["file"]):
		return OKResponse()
	if "download" in data and is_file_available(data["download"]):
		return FileResponse(Data.directory + data["download"])
	else:
		return NotFound()

def sync_nodes(request):
	print('\nsync node',request.remote[0],"\n>",end='')
	data = str(request.body,'utf-8')
	data = json.loads(data)

	for ip in data['nodes']:
		if ip == "0.0.0.0":
			data['nodes'][request.remote[0]] = {"ip":request.remote[0],"port":data['nodes'][ip]["port"],"active":True}
			del data['nodes'][ip]
			break
	if data["target_ip"] in data["nodes"]:
		del data["nodes"][data["target_ip"]]
	update_nodes(data['nodes'],lock_upload)
	return OKResponse()

@run_periodic
def discovery():
	print("\nstart discovery\n>",end='')
	data = {}
	data["nodes"] = get_nodes()["nodes"]
	for ip in get_cluster():
		if ip == "0.0.0.0":
			continue
		data["target_ip"] = ip
		Request.post("sync:%s:%s/discovery"%(ip,UDP_PORT),data=json.dumps(data))