from threading import Thread
import time

def run_periodic(func):
	def start():
		while True:
			func()
			time.sleep(60*60)
	def inner():
		Thread(target=start,args=()).start()
	inner()
