from shodan import Shodan
from shodan import *
import subprocess
import os
import os.path
import json
import mysql.connector
from contextlib import closing
from pexpect import pxssh
from datetime import datetime

def scan_asset():
	try:

		os.system("rm -rf /opt/projetmaster-master/ressource/vuln/* ; rm -rf /opt/projetmaster-master/ressource/json/*")

		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			# Base Mac UP
			mycursor.execute("SELECT * FROM macAdd WHERE isUp = 1;")
			baseMac = mycursor.fetchall()

			# Base Mac
			mycursor.execute("SELECT * FROM macAdd;")
			baseMacAll = mycursor.fetchall()

			# Api Key Shodan
			mycursor.execute("SELECT apiKey FROM mailCreds WHERE id = 1;")
			listapiKey = mycursor.fetchall()

			# Dump Base in File for Report
			fichierMAC = open("/opt/projetmaster-master/ressource/fichierMAC", "w")
			for device in baseMacAll:
				fichierMAC.write("" + str(device[0]) + " " + str(device[1].decode('utf-8')) + " " + str(device[2].decode('utf-8')) + " " + str(device[3].decode('utf-8')) + " " + str(device[4].decode('utf-8')) + " " + str(device[5]) + "\n")
			fichierMAC.close()

			# Decode queries
			apikey = [x[0].decode('utf-8') for x in listapiKey]
			list_device = [x[1].decode('utf-8') for x in baseMac]
			list_ip = [x[2].decode('utf-8') for x in baseMac]

			# @IP Public
			ip_publique = "curl ifconfig.io 2>/dev/null"
			public_ip = os.popen(ip_publique).read()
			public_ip = public_ip.replace('\n', '')

			# Scan Shodan IP Pulic
			reportScanGlobal = open("/opt/projetmaster-master/ressource/report/report_Scan", "w")
			for key in apikey:
				try:
					api = Shodan(key)
					results = api.host(public_ip)
					# result = str(results)
					reportScanGlobal.write('\nFound result for public IP ' + public_ip + ' on Shodan : \n' + result + '\n')
				except Exception as e:
					reportScanGlobal.write('\nShodan public IP scan : No Result\n')
			reportScanGlobal.close()

			# Scan By Device in Base
			for device in baseMac:
				reportScan = open("/opt/projetmaster-master/ressource/report/report_Scan_" + device[1].decode('utf-8'), "w")
				reportScan.write('\n[[ ' + device[1].decode('utf-8') + ' ]]')
				if device[2].decode('utf-8') == 'Not Found':
					mycursor.execute("SELECT user,pass FROM defaultPass WHERE device LIKE '" + device[1].decode('utf-8') + "'")
					creds_list = mycursor.fetchall()
				else:
					mycursor.execute("SELECT user,pass FROM defaultPass WHERE device LIKE '%" + device[2].decode('utf-8') + "%' OR device LIKE '%" + device[1].decode('utf-8') + "%'")
					creds_list = mycursor.fetchall()

				reportScan.write('\n-- Default Credentials --\n')
				for credentials in creds_list:
					try:
						conn = pxssh.pxssh()
						hostname = device[3].decode('utf-8')
						username = credentials[0].decode('utf-8')
						password = credentials[1].decode('utf-8')
						conn.login(hostname, username, password)
						reportScan.write("\n	WARNING ! Default credentials found for " + device[1].decode('utf-8') + " with user=" + username + " and password=" + password)
					except pxssh.ExceptionPxssh as e:
						reportScan.write("\nNo result for " + device[1].decode('utf-8') + " with user=" + username + " and password=" + password)

				command = "nmap -sS -T4 " + device[3].decode('utf-8') + " -oX /opt/projetmaster-master/ressource/nmap_" + device[1].decode('utf-8') + ".xml 2>/dev/null"
				open_port = os.popen(command).read()
				open_port = open_port.splitlines()

				reportScan.write('\n-- Open Port --\n')
				# Write open port in report
				for x in range(0,len(open_port)):
					if x > 3 and x < len(open_port) - 3:
						reportScan.write("\t" + open_port[x] + "\n")

				search_nmap = "searchsploit --nmap /opt/projetmaster-master/ressource/nmap_" + device[1].decode('utf-8') + ".xml -j > /opt/projetmaster-master/ressource/json/exploit_nmap_" + device[1].decode('utf-8') + " 2>/dev/null"
				os.system(search_nmap)

				# Scan Searchsploit from Nmap data
				search_model = "searchsploit " + device[1].decode('utf-8') + " -j > /opt/projetmaster-master/ressource/json/exploit_" + device[1].decode('utf-8')
				os.system(search_model)
				# Parse JSON obj
				jsonList = []
				# print("Started Reading JSON file which contains multiple JSON document")
				# Replace new line
				parsedJson = ""
				jsonToParse = open('/opt/projetmaster-master/ressource/json/exploit_nmap_' + device[1].decode('utf-8'))
				for line in jsonToParse:
					stripped_line = line.rstrip()
					parsedJson += stripped_line
				jsonToParse.close()

				jsonToParse = open('/opt/projetmaster-master/ressource/json/exploit_nmap_' + device[1].decode('utf-8'), 'w')
				jsonToParse.write(parsedJson)
				jsonToParse.close()

				# Seperate obj
				replacedJson = ""
				jsonToParse = open('/opt/projetmaster-master/ressource/json/exploit_nmap_' + device[1].decode('utf-8'))
				for line in jsonToParse:
					stripped_line = line.replace('}{', '}\n{')
					replacedJson += stripped_line
				jsonToParse.close()

				jsonToParse = open('/opt/projetmaster-master/ressource/json/exploit_nmap_' + device[1].decode('utf-8'), 'w')
				jsonToParse.write(replacedJson)
				jsonToParse.close()

				with open('/opt/projetmaster-master/ressource/json/exploit_nmap_' + device[1].decode('utf-8')) as f:
				    for jsonObj in f:
				        jsonDict = json.loads(jsonObj)
				        jsonList.append(jsonDict)

				# print("Printing each JSON Decoded Object")
				for nmapSearch in jsonList:
					for vuln in nmapSearch['RESULTS_EXPLOIT']:
						with open('/opt/projetmaster-master/ressource/vuln/exploit_nmap_' + device[1].decode('utf-8'), 'a') as vuln_model_1:
							vuln_model_1.write(str(vuln['Date']) + " " + str(vuln['Title']) + "\n")
					for vuln in nmapSearch['RESULTS_SHELLCODE']:
						with open('/opt/projetmaster-master/ressource/vuln/exploit_nmap_' + device[1].decode('utf-8'), 'a') as vuln_model_2:
							vuln_model_2.write(str(vuln['Date']) + " " + str(vuln['Title']) + "\n")

				with open('/opt/projetmaster-master/ressource/json/exploit_' + device[1].decode('utf-8')) as json_model_2:
					data_model_2 = json.load(json_model_2)

					for vuln in data_model_2['RESULTS_EXPLOIT']:
						with open('/opt/projetmaster-master/ressource/vuln/exploit_' + device[1].decode('utf-8'), 'a') as vuln_model_3:
							vuln_model_3.write(str(vuln['Date']) + " " + str(vuln['Title']) + "\n")
					for vuln in data_model_2['RESULTS_SHELLCODE']:
						with open('/opt/projetmaster-master/ressource/vuln/exploit_' + device[1].decode('utf-8'), 'a') as vuln_model_4:
							vuln_model_4.write(str(vuln['Date']) + " " + str(vuln['Title']) + "\n")
				reportScan.close()
		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass
	pass
scan_asset()