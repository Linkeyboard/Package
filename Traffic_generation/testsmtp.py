from email.mime.text import MIMEText

def sendemail(sendmessage='hello, send by Python...'):
	msg = MIMEText(sendmessage, 'plain', 'utf-8')

	# 输入Email地址和口令:
	from_addr = '403257745@qq.com'
	password = 'atwrtbsitvsqbjca'    # 授权码
	# 输入收件人地址:
	to_addr = 'lk@acm.hitwh.edu.cn'
	# 输入SMTP服务器地址:
	smtp_server = 'smtp.qq.com'
	

	import smtplib
	server = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()




	return 'SendSuccessfully'
