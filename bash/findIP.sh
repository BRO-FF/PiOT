#!/bin/bash

# FIND IP
# Find IP files
if [ -e /tmp/fichierIP ]; then
	rm /tmp/fichierIP
fi

# excludeIP=$(ip route | grep -oP '([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])' | sort -u | tr '\n' ' ')
# excludeIP=${excludeIP::-1}
# Parse file
grep -oP --exclude='lastlog' --exclude='*.gz' --exclude='*.1' --exclude='dpkg*' '([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])' /var/log/*log* 2>/dev/null | cut -d ":" -f 2 | sort -u > /tmp/fichierIP

# Diff between files
result=$(comm -23 <(sort /tmp/fichierIP) <(sort $PATHUSER/../ressource/fichierIP))

if [ -z "$result" ]
then
	echo "---" >> $PATHUSER/../logs/report
	echo "FindIP : OK" >> $PATHUSER/../logs/report
	echo "---" >> $PATHUSER/../logs/report
else
	echo "---" >> $PATHUSER/../logs/report
	echo "New IP found" >> $PATHUSER/../logs/report
	echo "---" >> $PATHUSER/../logs/report

	for i in $result; do
		# j=$(echo "${i//./$'\.'}")
		# grep "$i" /var/log/fail2ban.log | awk '{print $10,$11,$7,$8}' >> $PATHUSER/../logs/report
		grep "$i" /var/log/auth.log | awk '{print $1,$2,$3,$6,$7,$8,$9}' >> $PATHUSER/../logs/report
		echo "---" >> $PATHUSER/../logs/report
	done

	# echo $result | tr ' ' '\n' >> $PATHUSER/report/reportManage
	echo $result | tr ' ' '\n' >> $PATHUSER/../ressource/fichierIP
fi