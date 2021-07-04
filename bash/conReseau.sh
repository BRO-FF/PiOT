#!/bin/bash
#3
conReseau() {
	#Establish
	iptables -A INPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
	iptables -A OUTPUT -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#Ping
	iptables -A OUTPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#DNS
	iptables -A OUTPUT -p udp --dport 53 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	iptables -A INPUT -p udp --dport 53 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#NTP
	iptables -A OUTPUT -p udp --dport 123 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#DHCP
	iptables -A OUTPUT -p udp --dport 67 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#HTTPS
	iptables -A OUTPUT -p tcp --dport 443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	#HTTPS
	iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
	#HTTP
	iptables -A OUTPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	# Accept Mysql
	iptables -A INPUT -p tcp --dport 3306 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	# WEB GUI
	iptables -A INPUT -p tcp --dport 8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

	iptables -N EXTIP
	iptables -A FORWARD -i wlan0 -j EXTIP
	# iptables -A EXTIP -d 91.198.174.192 -j DROP

	iptables -N MACAUTH
	iptables -A EXTIP -i wlan0 -j MACAUTH

	# Forward du lan 10.10.0.0
	iptables -A MACAUTH -m state --state RELATED,ESTABLISHED -j ACCEPT
	#iptables -A MACAUTH -o eth0 -s 10.10.0.0/24 -j ACCEPT
	iptables -A MACAUTH -s 10.10.0.0/24 -d 192.168.1.0/24 -j DROP
	# Forbid wlan0
	iptables -A MACAUTH -i wlan0 -p tcp -j DROP
	# Enable NAT
	iptables -t nat -A POSTROUTING -s 10.10.0.0/24 -o eth0 -j MASQUERADE
	# Allow IOT to internet but not to main home network

	
}
conReseau