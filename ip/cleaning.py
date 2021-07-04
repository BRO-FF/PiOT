import mysql.connector
import os
from contextlib import closing

def clean_base():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)
		# Extract base
		with closing( mydb.cursor() ) as mycursor:
			
			mycursor.execute("DROP TABLE ext_access;")
			mydb.commit()

			mycursor.execute("CREATE TABLE ext_access ( id int NOT NULL AUTO_INCREMENT, ipExt varchar(32), malicious varchar(32), referer varchar(32), PRIMARY KEY (id));")
			mydb.commit()
			
		# Every Day Cleaning
		ziping = "scanZip=$(ls /opt/projetmaster-master/logs/tshark/) ; for file in $scanZip ; do gzip /opt/projetmaster-master/logs/tshark/$file ; done"
		mving = "scanZiped=$(ls /opt/projetmaster-master/logs/tshark/) ; for file in $scanZiped ; do mv /opt/projetmaster-master/logs/tshark/$file /opt/projetmaster-master/logs/last-week/$file ; done"
		os.system(ziping)
		os.system(mving)
		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	except Exception as e:
		raise e
		return False
	finally:
		mydb.close()
		pass
clean_base()