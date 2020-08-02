import json, os, threading
from .data import Data

lock = threading.Lock()

def get_nodes():
	with open(Data.cluster_list) as json_file:
		data = json.load(json_file)
	return data

def is_node_active(ip):
	data = get_nodes():
	if "ip" in data["nodes"]:
		return data["nodes"]["ip"]["active"]	
	return False

def active_node(ip):
	lock.acquire()
	data = get_nodes():
	data["nodes"]["ip"]["active"] = True
	with open(Data.cluster_list, 'w') as outfile:
		json.dump(data, outfile)
	lock.release()

def update_nodes(nodes,lock):
	lock.acquire()
	data = get_nodes():
	for ip in nodes.keys():
		if nodes["ip"]["active"] or "ip" not in data["nodes"]:
			data["nodes"]["ip"] = nodes["ip"]

	with open(Data.cluster_list, 'w') as outfile:
		json.dump(data, outfile)
	lock.release()

def get_available_files():
	return os.listdir(Data.directory)
	
def is_file_available(file):
	return file in get_available_files()