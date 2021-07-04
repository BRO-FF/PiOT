import os
import mysql.connector
from contextlib import closing
from datetime import datetime
from virustotal_python import Virustotal
from pprint import pprint
from base64 import urlsafe_b64encode
import json
vtotal = Virustotal(API_KEY="xxx", API_VERSION="v3")

def scan_asset_network():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			# Base Mac
			mycursor.execute("SELECT * FROM macAdd;")
			base_mac = mycursor.fetchall()

			# Base Ip
			mycursor.execute("SELECT ipExt FROM ext_access;")
			ext_access = mycursor.fetchall()
			ip_ext = [x[0].decode('utf-8') for x in ext_access]

			# Time
			nowIs = datetime.now()
			timeIs = nowIs.strftime("%d_%m_%Y_%H_%M_%S")
			
			# Load VT Api
			
			# Network Traffic Analysis
			for deviceAll in base_mac:
				
				reportScan = open("/opt/projetmaster-master/ressource/report/report_Scan_" + deviceAll[1].decode('utf-8'), "a")
				searchLogs = "grep -oP '([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])' /opt/projetmaster-master/logs/tshark/" + deviceAll[1].decode('utf-8') + "* 2>/dev/null | cut -d ':' -f2 | grep -v '8.8.8.8' | grep -v '10.10.0.1'| grep -v '" + deviceAll[3].decode('utf-8') + "' | sort -u"
				resultLogs = os.popen(searchLogs).read()
				# print(resultLogs)

				if resultLogs != "":
					reportScan.write('\n-- External Access --\n')
					reportScan.write(resultLogs)

				reportScan.close()

				tsharkRun = "/usr/bin/tshark -i wlan0 -a duration:60 host " + deviceAll[3].decode('utf-8') + " > /opt/projetmaster-master/logs/tshark/" + deviceAll[1].decode('utf-8') + "_dump_" + timeIs + " 2>/dev/null &"
				os.system(tsharkRun)

				# New Ip Identified
				logs = resultLogs.split('\n')
				del logs[-1]
				result = list(set(logs) - set(ip_ext))
				# Scan and insert Ip in base
				for ipExt in result:
					try:
						url_id = urlsafe_b64encode(ipExt.encode()).decode().strip("=")
						analysis_resp = vtotal.request(f"urls/{url_id}")
						response = analysis_resp.json()
						pass
					except VirustotalError:
						pass

					if response['data']['attributes']['total_votes']['malicious'] > response['data']['attributes']['total_votes']['harmless']:
						mycursor.execute("INSERT INTO ext_access (ipExt,malicious,referer) VALUES ('" + str(ipExt) + "','MALICIOUS', '" + deviceAll[1].decode('utf-8') + "') ")
						mydb.commit()
					elif response['data']['attributes']['total_votes']['malicious'] < response['data']['attributes']['total_votes']['harmless']:
						mycursor.execute("INSERT INTO ext_access (ipExt,malicious,referer) VALUES ('" + str(ipExt) + "','Harmless', '" + deviceAll[1].decode('utf-8') + "') ")
						mydb.commit()
					else:
						mycursor.execute("INSERT INTO ext_access (ipExt,malicious,referer) VALUES ('" + str(ipExt) + "','Undefined', '" + deviceAll[1].decode('utf-8') + "') ")
						mydb.commit()

		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	except NameError:
		return False
		pass
	finally:
		mydb.close()
		pass
	pass
scan_asset_network()