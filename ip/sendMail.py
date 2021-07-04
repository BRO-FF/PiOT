# your Gmail account
import smtplib
import os
import mysql.connector

def send_mail():
	# Connector mysql
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="corpus",
	  password="toor",
	  database="corpus"
	)
	mycursor = mydb.cursor(buffered=True)

	try:
		mycursor.execute("SELECT mailFrom,mailTo,appPass FROM mailCreds WHERE id=1 ;")
		records = mycursor.fetchall()
	except mysql.connector.errors.ProgrammingError:
		return False
	pass

	# Mail var
	for item in records:
		mailFrom = item[0]
		mailTo = item[1]
		appPass = item[2]

	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login(mailFrom, appPass)

	catManage = 'cat /opt/projetmaster-master/logs/report'
	body = os.popen(catManage).read()

	# message to be sent
	message = "\r\n".join([
	  "From: PIOT",
	  "To: " + mailTo + "",
	  "Subject: Maintenance Report",
	  "",
	 "" + body  + ""
	  ])

	# sending the mail
	s.sendmail(mailFrom, mailTo, message)

	# terminating the session
	s.quit()
	return True

if __name__ == '__main__':
    send_mail()