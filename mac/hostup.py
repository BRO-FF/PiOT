import mysql.connector
from contextlib import closing
import os

def host_is_up():

	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)
		
		with closing( mydb.cursor(prepared=True) ) as mycursor:
			mycursor.execute("SELECT ipA FROM macAdd;")
			listIP = mycursor.fetchall()

			for ip in listIP:
				HOST_UP  = True if os.system("ping -c 1 -w 2 " + str(ip[0].decode('utf-8'))) == 0 else False
				mycursor.execute("UPDATE macAdd SET isUp=" + str(HOST_UP) + " WHERE ipA='" + str(ip[0].decode('utf-8')) + "';")
				mydb.commit()

	except mysql.connector.errors.ProgrammingError:
		errorC = "No @MAC found in the base"
		return errorC
	except mysql.connector.errors.OperationalError:
		return "OperationalError"
	finally:
		mydb.close()
		pass
host_is_up()