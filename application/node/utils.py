import json, os

self.lock = threading.Lock()

def get_nodes():
	with open('application/configs/nodes.json') as json_file:
    	data = json.load(json_file)
    return data["nodes"]

def update_nodes(nodes):
	self.lock.acquire()
	current_nodes = get_nodes()["nodes"]
	for node in current_nodes:
		if node not in nodes:
			nodes.append(node)
	with open('application/configs/nodes.json', 'w') as outfile:
    	json.dump({"nodes":nodes}, outfile)
	self.lock.release()

def get_available_files():
	return os.listdir('application/files')
	
def is_file_available(file):
	return file in get_available_files()