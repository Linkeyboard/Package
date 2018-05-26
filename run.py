from flask import Flask 
from flask import render_template
from flask import request
from flask import make_response,Response
from Traffic_generation.http_traffic_generation import scapy_http
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
        p = Package(dst = host, num = int(num), protocol = "HTTP", flow = 0, time = nowTime)
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
        p = Package(dst = dsthost, num = int(qdcount), protocol = "DNS", flow = 0, time = nowTime)
        db_session.add(p) 
        db_session.commit()
        dns_packets(srchost = srchost, dsthost = dsthost, qdcount = int(qdcount), qname = qname)

    return render_template('dns.html')

@app.route('/ddos',methods=['GET','POST'])
def Choose_Ddos():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        num = request.form['num']   
        global pooltmp
        try:
            for i in range(2):
                pooltmp.apply_async(synFlood)
        except ValueError:
            pooltmp = Pool(4)
            for i in range(2):
                pooltmp.apply_async(synFlood)
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

if __name__ == "__main__":
    app.run(debug = True)
