import http.client as hc
import time
from scapy.all import *



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
    t = random.randint(1, 20000)
    while(num):
       a = IP()/TCP(sport = t)/"GET / HTTP/1.0\r\n\r\n"
       t = (t + 1) % 20000
       send(a)
       num = num - 1
       time.sleep(delay)


def scapy_tcp(host = "127.0.0.1", port = 8000, delay = 0, num = 1):
    t = random.randint(1, 20000)
    while(num):
       a = IP()/TCP(sport = t)
       t = (t + 1) % 20000
       send(a)
       num = num - 1
       time.sleep(delay)


def scapy_udp(host = "127.0.0.1", port = 8000, delay = 0, num = 1):
    t = random.randint(1, 20000)
    while(num):
       a = IP()/UDP(sport = t)
       t = (t + 1) % 20000
       send(a)
       num = num - 1
       time.sleep(delay)


if __name__ == "__main__":
    scapy_http(delay = 0.2, num = 10)
