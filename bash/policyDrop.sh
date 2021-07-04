#!/bin/bash
#6
policyDrop() {
	echo -e "Drop policy : "
	iptables -P INPUT DROP
	iptables -P FORWARD DROP
	iptables -P OUTPUT DROP
	echo -e "Policy dropped"
}
policyDrop