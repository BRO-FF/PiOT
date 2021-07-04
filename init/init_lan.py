import os
import getpass
import shodan
import subprocess
import mac.APImysql

def write_find_file():
	fichierIP = "./bash/addFichierIP"
	os.system(fichierIP)

	# fichierSUID = "./bash/addFichierSUID"
	# os.system(fichierSUID)
	pass

def install_searchsploit():
	cloneRep = "git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb"
	linkSploit = "ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit"

	os.system(cloneRep)
	os.system(linkSploit)
	pass

def create_user_cherrypy():
	addUser = "adduser --no-create-home --system --disabled-password -gid 0 -s /bin/bash cherrypy"
	os.system(addUser)
	pass

def write_config_file():
	# HOSTAPD
	ssid = input("SSID : ")
	passwd = getpass.getpass("Password : ")
	hostConf = """interface=wlan0
driver=nl80211
ssid=""" + ssid + """
hw_mode=g
channel=11
wpa=2
wpa_passphrase=""" + passwd + """
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
wpa_ptk_rekey=600"""

	hostapd = open("/etc/hostapd/hostapd.conf","a")
	hostapd.write (hostConf)
	hostapd.close()
	
	# DHCPD
	dhcpConf = """log-facility local7;
subnet 10.10.0.0 netmask 255.255.255.0 {
range 10.10.0.100 10.10.0.150;
default-lease-time 600;
max-lease-time 7200;
option domain-name-servers 8.8.8.8;
option routers 10.10.0.1;
option subnet-mask 255.255.255.0;
interface wlan0;
}"""

	dhcpd = open("/etc/dhcp/dhcpd.conf","a")
	dhcpd.write (dhcpConf)
	dhcpd.close()

	# dhcpLog = "touch /var/log/dhcpd.log ; chown syslog:adm /var/log/dhcpd.log ; chmod 0640 /var/log/dhcpd.log"
	# os.system(dhcpLog)

	sysctl = open("/etc/sysctl.conf","a")
	sysctl.write ("net.ipv4.ip_forward=1")
	sysctl.close()

	# ISC-DHCP-SERVER
	isc = open("/etc/default/isc-dhcp-server", "a")
	isc.close()
	isc = open("/etc/default/isc-dhcp-server", "r")

	new_isc = ""
	for line in isc:
		stripped_line = line.strip()
		new_line = stripped_line.replace('INTERFACESv4=""', 'INTERFACESv4="wlan0"')
		new_isc += new_line +"\n"
	isc.close()

	isc = open("/etc/default/isc-dhcp-server", "w")
	isc.write(new_isc)
	isc.close()

	syslog = open("/etc/rsyslog.conf", "a")
	syslog.write("local7.*          /var/log/dhcpd.log")
	syslog.close()

	# DNSMASQ
	dns = open("/etc/default/dnsmasq", "a")
	dns.close()
	dns = open("/etc/default/dnsmasq", "r")

	new_dns = ""
	for line in dns:
		stripped_line = line.strip()
		new_line = stripped_line.replace('#ENABLED=1', 'ENABLED=1')
		new_dns += new_line +"\n"
	dns.close()

	dns = open("/etc/default/dnsmasq", "w")
	dns.write(new_dns)
	dns.close()

	# NETWORK
	interface_d = """# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

allow-hotplug eth0
auto eth0
iface eth0 inet dhcp
iface default inet dhcp

# IP ADDRESS FOR IOT FW #

allow-hotplug wlan0
auto wlan0
iface wlan0 inet static
hostapd /etc/hostapd/hostapd.conf
address 10.10.0.1
netmask 255.255.255.0"""
	hostapd = open("/etc/network/interfaces","w")
	hostapd.write (interface_d)
	hostapd.close()

	hosts = open("/etc/hosts.deny", "a")
	hosts.write("ALL: ALL EXCEPT 192.168.1., 10.10.0., 0.debian.pool.ntp.org, 1.debian.pool.ntp.org, 2.debian.pool.ntp.org, 3.debian.pool.ntp.org")
	hosts.close()

	# Reboot interfaces
	start_int = "ifconfig wlan0 up"
	os.system(start_int)

		
	print("ALL RIGHT IT\'S DONE !")
		# Reboot
		# rebootService = "service rsyslog restart ; service isc-dhcp-server restart"
