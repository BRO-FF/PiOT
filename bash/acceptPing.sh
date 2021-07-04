#!/bin/bash
#2
acceptPing() {
	iptables -D INPUT 1
	iptables -D OUTPUT 1
	iptables -D FORWARD 1
	
	read -e -p "Accept Ping ? [Y/N] " -i "Y" confActu
	if [[ $confActu == "Y" ]]; then
		#Limit ping
		iptables -A INPUT -p icmp -m recent --name BLACKLIST --set
		iptables -A INPUT -p icmp -m recent --name BLACKLIST --update --seconds 10 --hitcount 10 --rttl -j DROP
		iptables -A INPUT -p icmp -m recent --name BLACKLIST --update --seconds 10 --hitcount 7 --rttl -j LOG --log-level warning --log-prefix "PINGBLACKLIST"
		iptables -A INPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
	fi
	echo -e "Ping ok"
}
acceptPing