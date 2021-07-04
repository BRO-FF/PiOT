#!/bin/bash
installKnock() {
	read -e -p "Install knocking ? [Y/N] " -i "Y" choiceKnock
	if [[ choiceKnock == "Y" ]]; then
		read -e -p "Port to protect ? " -i "22" portSSH
		read -e -p "How manny port to knock ? " -i "3" nbrPort
		portDef=5050
		proDef="tcp"
		portKnock=()
		for (( i = 1; i < nbrPort+1; i++ )); do
			read -e -p "Port $i ? " -i "$portDef:$proDef" portKnock["$i"]
			let portDef++
		done

		echo "You chose ${portKnock[*]} "
		iptables -N KNOCKING
		iptables -A INPUT -i eth0 -j KNOCKING

		#GATE1
		g=1
		port1=$(echo ${portKnock[1]} | cut -d':' -f1)
		pro1=$(echo ${portKnock[1]} | cut -d':' -f2)
		iptables -N GATE$g
		iptables -A GATE$g -p $pro1 --dport $port1 -m recent --name AUTH$g --set -j DROP
		iptables -A GATE$g -j DROP
		unset portKnock[1]

		for numeroP in ${portKnock[*]}; do
			#GATEn+1
			let g++
			port=$(echo $numeroP | cut -d':' -f1)
			pro=$(echo $numeroP | cut -d':' -f2)
			iptables -N GATE$g
			iptables -A GATE$g -m recent --name AUTH$(($g-1)) --remove -j LOG --log-level warning --log-prefix "AUTH$(($g-1))VALID"
			iptables -A GATE$g -p $pro --dport $port -m recent --name AUTH$g --set -j DROP
			iptables -A GATE$g -j GATE1
			iptables -A KNOCKING -m recent --name AUTH$(($g-1)) --rcheck --seconds 10 -j GATE$g
		done

		#PASSED
		iptables -N PASSED
		iptables -A PASSED -m recent --name AUTH$g --remove -j LOG --log-level warning --log-prefix "AUTHVALID"
		iptables -A PASSED -p tcp --dport $portSSH -j ACCEPT
		iptables -A PASSED -j GATE1

		#KNOCKING
		iptables -A KNOCKING -m recent --name AUTH$g --rcheck --seconds 10 -j PASSED
		iptables -A KNOCKING -j GATE1

		echo -e "Knoking installed "
	else
		echo "Alright"
	fi
}
installKnock