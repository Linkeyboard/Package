from flask import Flask 
from flask import render_template
from flask import request
from flask import make_response,Response
from Traffic_generation.http_traffic_generation import scapy_http, scapy_tcp, scapy_udp
from Traffic_generation.dns_traffic_generation import dns_packets
from Traffic_generation.ddos import ddos
from Traffic_generation.SYNflood import synFlood
from database import db_session,init_db
import json
from models import Package
import datetime
from multiprocessing import Pool, Process

app = Flask(__name__)

pooltmp = Pool(4)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tmp')
def hello():
    return render_template('tmp.html')

@app.route('/http',methods=['GET','POST'])
def Choose_Http():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        delay = request.form['delay']
        num = request.form['num']	
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
        p = Package(dst = host, num = int(num), protocol = "HTTP", flow = int(int(num) * 58), time = nowTime)
        db_session.add(p) 
        db_session.commit()
        scapy_http(host = host, port = int(port), delay = int(delay), num = int(num))
    return render_template('http.html')

@app.route('/dns',methods=['GET','POST'])
def Choose_Dns():
    if request.method == 'POST':
        srchost = request.form['srchost']
        dsthost = request.form['dsthost']
        qdcount = request.form['qdcount']
        qname = request.form['qname']   
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
        p = Package(dst = dsthost, num = int(qdcount), protocol = "DNS", flow = int(int(qdcount) * 56), time = nowTime)
        db_session.add(p) 
        db_session.commit()
        dns_packets(srchost = srchost, dsthost = dsthost, qdcount = int(qdcount), qname = qname)

    return render_template('dns.html')

@app.route('/tcp',methods=['GET','POST'])
def Choose_TCP():
    tcpflow = 56
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        delay = request.form['delay']
        num = request.form['num']	
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
        p = Package(dst = host, num = int(num), protocol = "TCP", flow = int(int(num) * 50), time = nowTime)
        db_session.add(p) 
        db_session.commit()
        scapy_tcp(host = host, port = int(port), delay = int(delay), num = int(num))
    return render_template('tcp.html')

@app.route('/udp',methods=['GET','POST'])
def Choose_UDP():
    udpflow = 44
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        delay = request.form['delay']
        num = request.form['num']	
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
        p = Package(dst = host, num = int(num), protocol = "UDP", flow = int(int(num) * 48), time = nowTime)
        db_session.add(p) 
        db_session.commit()
        scapy_udp(host = host, port = int(port), delay = int(delay), num = int(num))
    return render_template('udp.html')

@app.route('/ddos',methods=['GET','POST'])
def Choose_Ddos():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        num = request.form['num']   
        global pooltmp
        try:
            for i in range(2):
                pooltmp.apply_async(synFlood, args = (host, int(port), 0, 0))
        except ValueError:
            pooltmp = Pool(4)
            for i in range(2):
                pooltmp.apply_async(synFlood, args = (host, port,))
    return render_template('ddos.html')


@app.route('/combine',methods=['GET','POST'])
def Combine():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        delay = request.form['delay']
        num = request.form['num']	
        print(host, port, delay, num)

    return render_template('combine.html')
	
@app.route('/test',methods=['GET','POST'])
def test():
    return ""

showjson = ""
@app.route('/history',methods=['GET','POST'])
def history():
    findp = Package.query.filter().all()
    plist = []
    for p in findp:
        tmp = {}
        tmp['pid'] = p.pid
        tmp['dst'] = p.dst
        tmp['num'] = p.num
        tmp['flow'] = p.flow
        tmp['time'] = p.time
        tmp['protocol'] = p.protocol
        plist.append(tmp)
    
    global showjson
    jsontmp = {}
    jsontmp['code'] = 0
    jsontmp['msg'] = ""
    jsontmp['count'] = len(plist)
    jsontmp['data'] = plist
    print(jsontmp)
    json_p = json.dumps(jsontmp)
    showjson = json_p

    return render_template('history.html')


@app.route('/showdb', methods=['GET'])
def showdb():
    global showjson
    return showjson


@app.route('/stopddos',methods=['GET','POST'])
def stopddos():
    if request.method == 'POST':
        global pooltmp
        pooltmp.terminate()

    return ""

@app.route('/packagenum',methods=['GET','POST'])
def packagenum():
    return render_template('packagenum.html')

@app.route('/sendnum',methods=['GET','POST'])
def sendnum():
    if(request.method == "POST"):
        if request.form["Goodorder"] == "true":
            if request.form["HTTPck"] == "true":
                scapy_http(host = request.form["host"], port = int(request.form["port"]), num = int(request.form["HTTPnum"]))
            if request.form["DNSck"] == "true":
                dns_packets(dsthost = request.form["host"], qdcount = int(int(request.form["DNSnum"])))
            synFlood(tgt = request.form["host"], dport = int(request.form["port"]), num = int(request.form["DDOSnum"]))
        else:
            num1 = 0
            num2 = 0
            if request.form["HTTPck"] == "true":
                num1 = int(request.form["HTTPnum"])
            if request.form["DNSck"] == "true":
                num2 = int(request.form["DNSnum"])
            num3 = int(request.form["DDOSnum"])
            print(num1, num2, num3)
            while True:
                if num1 > 0:
                    scapy_http(host = request.form["host"], port = int(request.form["port"]), num = 1)
                    num1 = num1 - 1
                if num2 > 0:
                    dns_packets(dsthost = request.form["host"], qdcount = 1)
                    num2 = num2 - 1
                num3 = num3 - 1
                synFlood(tgt = request.form["host"], dport = int(request.form["port"]), num = 1)
                if num1 == 0 and num2 ==0 and num3 == 0:
                    break
    return ""


@app.route('/packageflow',methods=['GET','POST'])
def packageflow():

    return render_template('packageflow.html')


@app.route('/packagefre',methods=['GET','POST'])
def packagefre():
    return render_template('packagefre.html')


@app.route('/sendflow', methods=['GET','POST'])
def sendflow():
    if(request.method == "POST"):
        if request.form["Goodorder"] == "true":
            if request.form["HTTPck"] == "true":
                scapy_http(host = request.form["host"], port = int(request.form["port"]), num = int(int(request.form["HTTPflow"]) * 1024 / 76 + 0.5))
            if request.form["DNSck"] == "true":
                dns_packets(dsthost = request.form["host"], qdcount = int(int(request.form["DNSflow"]) * 1024 / 74 + 0.5))
            synFlood(tgt = request.form["host"], dport = int(request.form["port"]), num = int(int(request.form["DDOSflow"]) * 1024 / 56 + 0.5))
        else:
            num1 = 0
            num2 = 0
            if request.form["HTTPck"] == "true":
                num1 = int(request.form["HTTPflow"])
                num1 = int(num1 * 1024 / 76 + 0.5)
            if request.form["DNSck"] == "true":
                num2 = int(request.form["DNSflow"])
                num2 = int(num2 * 1024 / 74 + 0.5)
            num3 = int(request.form["DDOSflow"])
            num3 = int(num3 * 1024 / 56)
            while True:
                if num1 > 0:
                    scapy_http(host = request.form["host"], port = int(request.form["port"]), num = 1)
                    num1 = num1 - 1
                if num2 > 0:
                    dns_packets(dsthost = request.form["host"], qdcount = 1)
                    num2 = num2 - 1
                num3 = num3 - 1
                synFlood(tgt = request.form["host"], dport = int(request.form["port"]), num = 1)
                if num1 == 0 and num2 ==0 and num3 == 0:
                    break
    return ""


@app.route('/sendfre', methods=['GET','POST'])
def sendfre():
    if(request.method == "POST"):
        t1 = int(request.form["HTTPfre"])
        t2 = int(request.form["DNSfre"])
        t3 = int(request.form["DDOSfre"])
        t = int(request.form["Alltime"])
        print(t2, t)
        frepool = Pool(4)
        if request.form["HTTPck"] == "true":
            frepool.apply_async(scapy_http, args = (request.form["host"], int(request.form["port"]), t1, int(t/t1)))
        if request.form["DNSck"] == "true":
            frepool.apply_async(dns_packets, args = ("127.0.0.1", request.form["host"], int(t/t2), "www.qq.com", t2))
        frepool.apply_async(synFlood, args = (request.form["host"], int(request.form["port"]), int(t/t3), t3))
        frepool.close()
        frepool.join()
    return ""

if __name__ == "__main__":
    app.run(debug = True)
