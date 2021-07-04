from shodan import Shodan
from shodan import *
import subprocess
import os
from mac import APImysql
import mysql.connector
from contextlib import closing
from pexpect import pxssh

def shodan(api_key):
	try:
		curl_ip = "curl ifconfig.io 2>/dev/null"
		ipPublic = os.popen(curl_ip).read()
		api = Shodan(api_key)
		results = api.host(ipPublic)
	except Exception as error:
		return error
		
		pass
	return results

def shodan_ip(api_key, ip_search):
	try:

		api = shodan.Shodan(api_key)
		results = api.search(ip_search)

		if results['total'] == 0:
			result = "No result"
		else:
			result = str(results['total'])

		return result
	except shodan.exception.APIError:
		print("TimeOut try again")

def scan_asset():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			# Mysql queries
			mycursor.execute("SELECT * FROM macAdd WHERE isUp = 1;")
			mac_table = mycursor.fetchall()
			mycursor.execute("SELECT apiKey FROM mailCreds WHERE id = 1;")
			listapiKey = mycursor.fetchall()

		# Decode queries
		apikey = [x[0].decode('utf-8') for x in listapiKey]
		list_device = [x[1].decode('utf-8') for x in mac_table]
		list_ip = [x[2].decode('utf-8') for x in mac_table]

		# @IP Public
		ip_publique = "curl ifconfig.io 2>/dev/null"
		public_ip = os.popen(ip_publique).read()
		public_ip = public_ip.replace('\n', '')

		# Report file
		list_scan = open("/opt/projetmaster-master/ressource/fichierScan", "w")
		list_scan.write('-- Scan Asset Report --\n')
		
		# search_file = open("/opt/projetmaster-master/ressource/searchsploit", "w")
		# search_file.write('-- Searchsploit Scan Report --\n')
		# search_file.close()

		# Scan Shodan IP Pulic
		for key in apikey:
			try:
				api = Shodan(key)
				results = api.host(public_ip)
				# result = str(results)
				list_scan.write('\nFound result for public IP ' + public_ip + ' on Shodan : \n' + result + '\n')
			except Exception as e:
				list_scan.write('\nShodan public IP scan : No Result\n')

		# Open port from list IP
		i = 0
		for ip in list_ip:

			command = "nmap -sS -T4 " + ip + " -oX /opt/projetmaster-master/ressource/nmap.xml 2>/dev/null"
			open_port = os.popen(command).read()
			open_port = open_port.splitlines()

			list_scan.write("\n[[ " + list_device[i] + " ]]\n")
			
			# Searchsploit of port nmap scan
			# Empty if none
			search_nmap = "searchsploit --nmap /opt/projetmaster-master/ressource/nmap.xml 2>/dev/null"
			list_scan.write(os.popen(search_nmap).read() + "\n")

			# Searchsploit of device name
			search_device = "searchsploit " + list_device[i] + " 2>/dev/null"
			list_scan.write("\nSearchSploit : \n" + os.popen(search_device).read() + "\nNmap :\n")

			for x in range(0,len(open_port)):
				if x > 3 and x < len(open_port) - 2:
					list_scan.write("\t" + open_port[x] + "\n")
			i += 1

		list_scan.close()

		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass
	pass

def public_ip():
	nmap = 'nmap -sS "$(curl ifconfig.io 2>/dev/null)" | awk \'/^[0-9]/\''
	openPort = os.popen(nmap).read()
	return openPort
	pass

def port_open(ipToScan):
	#ipToScan = APImysql.select_ip_by_id(id)
	nmap = "nmap -sS " + ipToScan + " | awk '/^[0-9]/' | awk '{split($0,a,\"/\"); print a[1]}'"
	openPort = os.popen(nmap).read()
	return openPort

def attempt_con(ipToScan, macToSearch):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		base_mac = mac.display_base("all")

		for device in base_mac:

			with closing( mydb.cursor(prepared=True) ) as mycursor:
				# if not (device[1] or device[2]) or not (device[1] and device[2]):
				if not device[1]:
					mycursor.execute("SELECT user,pass FROM defaultPass WHERE device LIKE '" + device[2] + "'")
					creds_list = mycursor.fetchall()
				elif not device[2]:
					mycursor.execute("SELECT user,pass FROM defaultPass WHERE device LIKE '" + device[1] + "'")
					creds_list = mycursor.fetchall()
				else:
					mycursor.execute("SELECT user,pass FROM defaultPass WHERE device LIKE '%" + device[2] + "%' OR LIKE '%" + device[1] + "%'")
					creds_list = mycursor.fetchall()

				for credentials in creds_list:
					try:
						conn = pxssh.pxssh()
						hostname = device[3]
						username = credentials[0].decode('utf-8')
						password = credentials[1].decode('utf-8')
						conn.login(hostname, username, password)
						print('SUCCESS')
					except pxssh.ExceptionPxssh as e:
						print('FAILED')
					pass

		return True
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

# Snif
every 60 min
for ip_UP in base_mac:
	command = "/usr/bin/tshark -i wlan0 -a duration:30 host " + ip + " > /opt/projetmaster-master/logs/tshark/" + device + "_dump_" + date
	os.system(command)
