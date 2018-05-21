from scapy.all import *

def dns_packets(srchost = '127.0.0.1', dsthost = '127.0.0.1', qdcount = 1, qname = 'www.qq.com'):
    while (qdcount):
        qdcount -= 1
        a = IP(dst = dsthost,src = srchost)
        b = UDP()
        c = DNS(id=1,qr=0,opcode=0,tc=0,rd=1,qdcount=qdcount,ancount=0,nscount=0,arcount=0)
        c.qd=DNSQR(qname=qname,qtype=1,qclass=1)
        p = a/b/c
        send(p)


if __name__ == "__main__":
    dns_packets()
