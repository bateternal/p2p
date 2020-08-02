from threading import Thread
import time

from settings import *

def run_periodic(func):
	def start():
		while True:
			func()
			time.sleep(PERIOD_DICOVERY_TIME)
	def inner():
		Thread(target=start,args=()).start()
	inner()
