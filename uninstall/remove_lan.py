import os
import getpass
from os import path
import mac.APImysql

def remove_lan():
	apt = "cat requirement-apt | xargs apt autoremove --purge -y"
	os.system(apt)

	pip = "pip3 uninstall -y -r requirement-pip"
	os.system(pip)

	if input("Delete file ? [Y/N] : ") == "Y":
		# HOSTAPD
		# ssid = input("SSID : ")
		# passwd = getpass.getpass("Password : ")

		if path.exists('/etc/hostapd/hostapd.conf') == True:
			hostConf = "rm /etc/hostapd/hostapd.conf"
			os.system(hostConf)
		pass
		
		# DHCPD
		hostConf = """option domain-name "example.org";
option domain-name-servers ns1.example.org, ns2.example.org;
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;}"""

		hostapd = open("/etc/dhcp/dhcpd.conf","w")
		hostapd.write (hostConf)
		hostapd.close()

		# SYSCTL
		reading_file = open("/etc/sysctl.conf", "r")

		new_file_content = ""
		for line in reading_file:
			stripped_line = line.strip()
			new_line = stripped_line.replace('net.ipv4.ip_forward=1', '')
			new_file_content += new_line +"\n"
		reading_file.close()

		writing_file = open("/etc/sysctl.conf", "w")
		writing_file.write(new_file_content)
		writing_file.close()

		# RSYSLOG
		reading_file = open("/etc/rsyslog.conf", "r")

		new_file_content = ""
		for line in reading_file:
			stripped_line = line.strip()
			new_line = stripped_line.replace('local7.*          /var/log/dhcpd.log', '')
			new_file_content += new_line +"\n"
		reading_file.close()

		writing_file = open("/etc/rsyslog.conf", "w")
		writing_file.write(new_file_content)
		writing_file.close()

		fileInt = """# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

iface default inet dhcp
allow-hotplug eth0
auto eth0"""
		hostapd = open("/etc/network/interfaces","w")
		hostapd.write (fileInt)
		hostapd.close()

	if input("Delete tables ? [Y/N] : ") == "Y":
		mac.APImysql.delete_table_default_pass()
		mac.APImysql.delete_table_mac()
		print("Table created")

		print("ALL DONE ! EVERYTHING HAS BEEN REMOVED")
		pass
	pass