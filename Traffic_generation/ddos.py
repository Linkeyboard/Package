import http.client as hc
import time
from multiprocessing import Pool
import os, time, random
from Traffic_generation.SYNflood import synFlood

def ddos(host = "127.0.0.1", port = 8000, num = 1):
	p = Pool(num)
	for i in range(num):
		p.apply_async(synFlood, args = (host, port,))
	p.close()
	p.join()	
	#http_traffic_generation(delay = 0.2, num = 10)
