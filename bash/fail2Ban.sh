#!/bin/bash
#4
fail2Ban() {
	read -e -p "Install fail2ban ? [Y/N] " -i "Y" failBan
	if [[ $failBan == "N" ]]; then
		iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
	else
		while [[ $failBan == "Y" ]]; do
			read -e -p "Port to protect ? " -i "22" protPort
			if [[ $failBan == "Y" ]]; then
				# Limit connexion by secondes
				iptables -A INPUT -i eth0 -p tcp --syn --dport $protPort -m recent --name FAILTOBAN --set
				iptables -A INPUT -i eth0 -p tcp --syn --dport $protPort -m recent --name FAILTOBAN --rcheck --seconds 300 --hitcount 10 -j DROP
				iptables -A INPUT -i eth0 -p tcp --syn --dport $protPort -m recent --name FAILTOBAN --rcheck --seconds 300 --hitcount 7 -j LOG --log-level warning --log-prefix "FAILTOBAN"
				echo "The rules are installed"
			fi
			read -e -p "Configure another port ? " -i "N" failBan
		done

		echo -e "Alright "
	fi
}
fail2ban