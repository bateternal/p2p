import json, os, threading
from .data import Data

from .connection import Connection
from threading import Thread

from presentation.request import Request
lock = threading.Lock()
lock_node = threading.Lock()
def get_nodes():
	lock.acquire()
	with open(Data.node_config) as json_file:
		data = json.load(json_file)
	lock.release()
	return data
	

def is_node_active(ip):
	data = get_nodes()
	if "ip" in data["nodes"]:
		return data["nodes"]["ip"].get("active",False)	
	return False

def get_cluster():
	with open(Data.cluster_list) as json_file:
		data = json.load(json_file)
	return data["clusters"]

def update_cluster(clusters):
	current_cluster = get_cluster()
	for cluster in current_cluster:
		if cluster not in clusters:
			clusters.append(cluster)
	with open(Data.cluster_list, 'w') as outfile:
		json.dump({"clusters":clusters}, outfile)

def active_node(ip):
	lock.acquire()
	data = get_nodes()
	data["nodes"]["ip"]["active"] = True
	with open(Data.node_config, 'w') as outfile:
		json.dump(data, outfile)
	lock.release()

def update_nodes(nodes,lock):
	lock.acquire()
	data = get_nodes()
	for ip in nodes.keys():
		update_cluster([ip])
		
		if nodes[ip]["active"] or ip not in data["nodes"]:
			data["nodes"][ip] = nodes[ip]

	with open(Data.node_config, 'w') as outfile:
		json.dump(data, outfile)
	lock.release()

def get_available_files():
	return os.listdir(Data.directory)
	
def is_file_available(file):
	return file in get_available_files()

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
		if node["ip"] is not "0.0.0.0":
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
		print("\nfile %s not found\n>"%file,end='')