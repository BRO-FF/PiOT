#!/bin/bash
#1
flushRules() {
	echo -e "Removing the rules"
	iptables -F
	iptables -X
	iptables -P INPUT ACCEPT
	iptables -P OUTPUT ACCEPT
	iptables -P FORWARD ACCEPT
	iptables -A INPUT -i lo -j ACCEPT
	iptables -A OUTPUT -o lo -j ACCEPT
	echo -e "The rules are removed "
}
flushRules