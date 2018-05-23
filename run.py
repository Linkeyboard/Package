from flask import Flask 
from flask import render_template
from flask import request
from flask import make_response,Response
from Traffic_generation.http_traffic_generation import http_traffic_generation
from Traffic_generation.dns_traffic_generation import dns_packets
from Traffic_generation.ddos import ddos
from Traffic_generation.SYNflood import synFlood

import json

app = Flask(__name__)

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
        print(host, port, delay, num)
        http_traffic_generation(host = host, port = int(port), delay = int(delay), num = int(num))

    return render_template('http.html')

@app.route('/dns',methods=['GET','POST'])
def Choose_Dns():
    if request.method == 'POST':
        srchost = request.form['srchost']
        dsthost = request.form['dsthost']
        qdcount = request.form['qdcount']
        qname = request.form['qname']   
        dns_packets(srchost = srchost, dsthost = dsthost, qdcount = int(qdcount), qname = qname)

    return render_template('dns.html')

@app.route('/ddos',methods=['GET','POST'])
def Choose_Ddos():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        num = request.form['num']   
        ddos(host = host, port = int(port), num = int(num))

    return render_template('ddos.html')


@app.route('/combine',methods=['GET','POST'])
def Combine():
    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']
        delay = request.form['delay']
        num = request.form['num']	
        print(host, port, delay, num)
        http_traffic_generation(host = host, port = int(port), delay = int(delay), num = int(num))

    return render_template('combine.html')
	
if __name__ == "__main__":
    app.run(debug = True)