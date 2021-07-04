import mysql.connector
import os
from os import path
from pexpect import pxssh
import getpass
import hashlib
from contextlib import closing
import ip.sendMail

if path.exists('/var/log/dhcpd.log') == True:
	# Get new @Mac
	macBash = "tail /var/log/dhcpd.log 2>/dev/null | grep \"DHCPREQUEST\" | awk '{split($0,a,\"from\"); print a[2]}' | awk '{print $1}' | tail -1 | tr -d \"\n\" "
	newMac = os.popen(macBash).read()
	pass

def display_base(field):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)
		# Extract base
		with closing( mydb.cursor() ) as mycursor:
			mycursor.execute("SELECT * FROM macAdd;")
			records = mycursor.fetchall()

		# Dump device info in file for report to keep it updated
		fichierMAC = open("/opt/projetmaster-master/ressource/fichierMAC", "w")
		for device in records:
			fichierMAC.write("" + str(device[0]) + " " + str(device[1]) + " " + str(device[2]) + " " + str(device[3]) + " " + str(device[4]) + " " + str(device[5]) + "\n")
		fichierMAC.close()

		# ID
		nid = 0
		id_base = [x[nid] for x in records]
		# Device
		nde = 1
		device = [x[nde] for x in records]
		# Brand
		nub = 2
		brand = [x[nub] for x in records]
		# IP
		nip = 3
		ip = [x[nip] for x in records]
		# Mac
		nac = 4
		mac = [x[nac] for x in records]
		# IsUp
		nup = 5
		up = [x[nup] for x in records]

		# Return by args field
		if field == 'all':
			return records
		elif field == 'id':
			return id_base
		elif field == 'device':
			return device
		elif field == 'brand':
			return brand
		elif field == 'ip':
			return ip
		elif field == 'mac':
			return mac
		elif field == 'isup':
			return up
			# pass

	except mysql.connector.errors.ProgrammingError:
		errorC = "No @MAC found in the base"
		return errorC
	except mysql.connector.errors.OperationalError:
		return "OperationalError"
	finally:
		mydb.close()
		pass

def create_table():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor() ) as mycursor:

			mycursor.execute("CREATE TABLE defaultPass ( id int NOT NULL AUTO_INCREMENT, device varchar(32), user varchar(32), pass varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE macAdd ( id int NOT NULL AUTO_INCREMENT, device varchar(32), brand varchar(32), ipA varchar(32), macA varchar(32), isUp BOOLEAN, PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE passwd ( id int NOT NULL AUTO_INCREMENT, user varchar(32), pass varchar(100), salt varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE auth_ip ( id int NOT NULL AUTO_INCREMENT, ipAuth varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE mailCreds ( id int NOT NULL AUTO_INCREMENT, mailFrom varchar(32), mailTo varchar(32), appPass varchar(32), apiKey varchar(100), PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE ext_access ( id int NOT NULL AUTO_INCREMENT, ipExt varchar(32), malicious varchar(32), referer varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			mycursor.execute("CREATE TABLE ext_ban ( id int NOT NULL AUTO_INCREMENT, ipExt varchar(32), malicious varchar(32), referer varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			with open("ressource/defaultPass","r") as read_obj:
				for line in read_obj:
					unsplit = str(line).split(',')
					mycursor.execute("INSERT INTO defaultPass (device,user,pass) VALUES ('" + unsplit[0] + "','" + unsplit[1] + "','" + unsplit[2].strip('\n') + "') ")
					mydb.commit()
		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

def setup_send_mail(mailFrom, mailTo, appPass, apiKey):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'mailCreds';")
			records = mycursor.fetchall()
			
			if records == []:
				mycursor.execute("CREATE TABLE mailCreds ( id int NOT NULL AUTO_INCREMENT, mailFrom varchar(32), mailTo varchar(32), appPass varchar(32), apiKey varchar(100), PRIMARY KEY (id));")
				mydb.commit()

			try:
				mycursor.execute("INSERT INTO mailCreds (mailFrom,mailTo,appPass,apiKey) VALUES ('" + mailFrom + "','" + mailTo + "','" + appPass + "','" + apiKey + "') ")
				mydb.commit()
				# mydb.close()
			except mysql.connector.errors.ProgrammingError:
				return False
			pass

		config_send_mail = "./../bash/sendMail-config.sh"
		os.system(config_send_mail)

		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

def authorized_ip():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT * FROM auth_ip;")
			listAuth = mycursor.fetchall()
		return listAuth
	
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

def display_ban():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:
			mycursor.execute("SELECT * FROM ext_ban;")
			ExtBan = mycursor.fetchall()
			if ExtBan == []:
				return False
				pass
			return ExtBan
	
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

def display_ip():
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:
			mycursor.execute("SELECT * FROM ext_access;")
			ExtAccess = mycursor.fetchall()
		return ExtAccess
	
	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

# Add mac in sudo iptables and the base
def add_mac(addressM: str) -> bool:

	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT ipA FROM macAdd WHERE macA LIKE '%" + addressM + "%';")
			macExist = mycursor.fetchall()

			if macExist != []:
				return False

			addressM = addressM.lower()
			ipMac = "zgrep 'DHCPACK' /var/log/dhcpd.log | grep '" + addressM + "' | awk '{print $8}' | tail -n 1 | tr -d \"\n\" | tr -d '()'"
			ip_mac = os.popen(ipMac).read()

			deviceName = "zgrep 'DHCPACK' /var/log/dhcpd.log | grep '" + addressM + "' | awk '{print $11}' | sort -u | head -1 | tr -d \"\n\" | tr -d '()'"
			device = os.popen(deviceName).read()

			macRequest = "curl https://api.macvendors.com/" + addressM + " 2>/dev/null"
			vendor = os.popen(macRequest).read()
			device_brand = vendor.partition(' ')[0]
			device_brand = device_brand.replace(',', '')
			device_brand = device_brand.replace('.', '')

			if device_brand == '{"errors":{"detail":"No':
				device_brand = 'Not Found'

			insertDevice = "INSERT INTO macAdd (device,brand,ipA,macA) VALUES ('" + device + "','" + device_brand + "','" + ip_mac + "','" + addressM + "');"
			mycursor.execute(insertDevice)
			mydb.commit()

			mycursor.execute("SELECT id FROM macAdd WHERE ipA='" + ip_mac + "';")
			record = mycursor.fetchone()
			records = str(record).strip("[](),'")

			records = str(int(records) + 2)
			# 
			addMac = "sudo iptables -I MACAUTH " + records + " -i wlan0 -m mac --mac-source " + addressM + " -j ACCEPT"
			os.system(addMac)
		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

	# DELETE MAC FROM BASE
def delete_mac(id):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor() ) as mycursor:

			mycursor.execute("DELETE FROM macAdd WHERE id=" + id + ";")
			mydb.commit()

			id = str(int(id) + 2)
			delMac = "sudo iptables -D MACAUTH " + id + ""
			os.system(delMac)

			mycursor.execute("SELECT device,brand,ipA,macA,isUp FROM macAdd;")
			confTable = mycursor.fetchall()

			mycursor.execute("DROP TABLE macAdd;")
			mydb.commit()

			# Increment auto id database
			mycursor.execute("CREATE TABLE macAdd ( id int NOT NULL AUTO_INCREMENT, device varchar(32), brand varchar(32), ipA varchar(32), macA varchar(32), isUp BOOLEAN, PRIMARY KEY (id));")
			mydb.commit()

			for item in confTable:
				device = item[0]
				brand = item[1]
				ip = item[2]
				mac = item[3]
				isUP = item[4]
				mycursor.execute("INSERT INTO macAdd (device,brand,ipA,macA,isUp) VALUES ('" + device + "','" + brand + "','" + ip + "', '" + mac + "','" + str(isUP) + "')")
				mydb.commit()
				pass
			confTable = ""
		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	except Exception as e:
		raise e
		return False
	finally:
		mydb.close()
		pass

def add_ip(addrIP: str) -> bool:

	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT ipAuth FROM auth_ip WHERE ipAuth='" + addrIP + "';")
			macExist = mycursor.fetchall()

			if macExist != []:
				return False

			mycursor.execute("INSERT INTO auth_ip (ipAuth) VALUES ('" + addrIP + "');")
			mydb.commit()

			mycursor.execute("SELECT * FROM auth_ip;")
			added = mycursor.fetchall()

			hosts = open("/etc/hosts.deny", "w")
			hosts.write('ALL: ALL EXCEPT ')
			for ipAdd in added:
				hosts.write(str(ipAdd[1].decode('utf-8')) + ', ')
			hosts.close()

			with open('/etc/hosts.deny', 'rb+') as filehandle:
			    filehandle.seek(-1, os.SEEK_END)
			    filehandle.truncate()
			    filehandle.seek(-1, os.SEEK_END)
			    filehandle.truncate()

		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	finally:
		mydb.close()
		pass

def block_ip(ipToBlock):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT * FROM ext_access WHERE ipExt='" + ipToBlock + "';")
			banIp = mycursor.fetchall()

			mycursor.execute("DELETE FROM ext_access WHERE ipExt='" + ipToBlock + "';")
			mydb.commit()

			for item in banIp:
				ide = item[0]
				ipExt = item[1].decode('utf-8')
				malicious = item[2].decode('utf-8')
				referer = item[3].decode('utf-8')

				mycursor.execute("INSERT INTO ext_ban (ipExt,malicious,referer) VALUES ('" + ipExt + "', '" + malicious + "', '" + referer + "')")
				mydb.commit()
			removed = ""

			mycursor.execute("SELECT * FROM ext_ban WHERE ipExt='" + ipToBlock + "';")
			banned = mycursor.fetchall()
			for itm in banned:
				dropExt = "iptables -I EXTIP " + str(itm[0]) + " -d " + ipToBlock + " -j DROP"
				os.system(dropExt)

			# Increment auto id database
			mycursor.execute("SELECT * FROM ext_access;")
			incre = mycursor.fetchall()

			mycursor.execute("DROP TABLE ext_access;")
			mydb.commit()

			mycursor.execute("CREATE TABLE ext_access ( id int NOT NULL AUTO_INCREMENT, ipExt varchar(32), malicious varchar(32), referer varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			for item in incre:
				idM = item[0]
				ipExt = item[1].decode('utf-8')
				malicious = item[2].decode('utf-8')
				referer = item[3].decode('utf-8')
				mycursor.execute("INSERT INTO ext_access (ipExt,malicious,referer) VALUES ('" + ipExt + "','" + malicious + "','" + referer + "')")
				mydb.commit()
				pass
			incre = ""

		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	except Exception as e:
		raise e
		return False
	finally:
		mydb.close()
		pass

def unblock_ip(ipToUnBlock):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor(prepared=True) ) as mycursor:

			mycursor.execute("SELECT * FROM ext_ban WHERE ipExt='" + ipToUnBlock + "';")
			unBanIp = mycursor.fetchall()

			mycursor.execute("DELETE FROM ext_ban WHERE ipExt='" + ipToUnBlock + "';")
			mydb.commit()

			for item in unBanIp:
				ide = item[0]
				ipExt = item[1].decode('utf-8')
				malicious = item[2].decode('utf-8')
				referer = item[3].decode('utf-8')

				mycursor.execute("INSERT INTO ext_access (ipExt,malicious,referer) VALUES ('" + ipExt + "', '" + malicious + "', '" + referer + "');")
				mydb.commit()

				dropExt = "iptables -D EXTIP " + str(ide)
				os.system(dropExt)
			removed = ""

			# Increment auto id database
			mycursor.execute("SELECT * FROM ext_ban;")
			incre = mycursor.fetchall()

			mycursor.execute("DROP TABLE ext_ban;")
			mydb.commit()

			mycursor.execute("CREATE TABLE ext_ban ( id int NOT NULL AUTO_INCREMENT, ipExt varchar(32), malicious varchar(32), referer varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			for item in incre:
				idM = item[0]
				ipExt = item[1].decode('utf-8')
				malicious = item[2].decode('utf-8')
				referer = item[3].decode('utf-8')
				mycursor.execute("INSERT INTO ext_ban (ipExt,malicious,referer) VALUES ('" + ipExt + "','" + malicious + "','" + referer + "')")
				mydb.commit()
				pass
			incre = ""

		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	except Exception as e:
		raise e
		return False
	finally:
		mydb.close()
		pass

def delete_ip(id):
	try:
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="corpus",
		  password="toor",
		  database="corpus"
		)

		with closing( mydb.cursor() ) as mycursor:

			mycursor.execute("DELETE FROM auth_ip WHERE id=" + id + ";")
			mydb.commit()

			mycursor.execute("SELECT * FROM auth_ip;")
			removed = mycursor.fetchall()

			hosts = open("/etc/hosts.deny", "w")
			hosts.write('ALL: ALL EXCEPT ')
			for ipAdd in removed:
				hosts.write(str(ipAdd[1]) + ', ')
			hosts.close()

			with open('/etc/hosts.deny', 'rb+') as filehandle:
			    filehandle.seek(-1, os.SEEK_END)
			    filehandle.truncate()
			    filehandle.seek(-1, os.SEEK_END)
			    filehandle.truncate()

			mycursor.execute("DROP TABLE auth_ip;")
			mydb.commit()

			# Increment auto id database
			mycursor.execute("CREATE TABLE auth_ip ( id int NOT NULL AUTO_INCREMENT, ipAuth varchar(32), PRIMARY KEY (id));")
			mydb.commit()

			for item in removed:
				idM = item[0]
				ipAdd = item[1]
				mycursor.execute("INSERT INTO auth_ip (ipAuth) VALUES ('" + ipAdd + "')")
				mydb.commit()
				pass
			removed = ""
		return True

	except mysql.connector.errors.ProgrammingError:
		return False
	except Exception as e:
		raise e
		return False
	finally:
		mydb.close()
		pass