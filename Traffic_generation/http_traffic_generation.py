import http.client as hc
import time
from scapy.all import *


tmp = 1

def http_traffic_generation(host = "127.0.0.1", port = 8000, delay = 0, num = 1):
    h = hc.HTTPConnection(host, port)
    t = num
    while(num):
       num = num - 1
       h.request("GET", "/")
       r = h.getresponse()
       print(t - num, r.status, r.reason)
       time.sleep(delay)



def scapy_http(host = "127.0.0.1", port = 8000, delay = 0, num = 1):
    global tmp
    tmp = (tmp + 1) % 5000
    t = num
    while(num):
       a = IP()/TCP(sport = tmp)/"GET / HTTP/1.0\r\n\r\n"
       send(a)
       num = num - 1
       time.sleep(delay)




if __name__ == "__main__":
    scapy_http(delay = 0.2, num = 10)
