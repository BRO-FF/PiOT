#!/bin/bash

# Get directory path
export PATHUSER="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

echo "===============================" > $PATHUSER/../logs/report
date >> $PATHUSER/../logs/report
echo -e "===============================
Base MAC
-------------------------------
id	Device	Ip	Mac	IsUp" >> $PATHUSER/../logs/report
if [[ -e $PATHUSER/../ressource/fichierMAC ]]; then
	cat $PATHUSER/../ressource/fichierMAC >> $PATHUSER/../logs/report
fi

echo -e "
-------------------------------
Scan
-------------------------------" >> $PATHUSER/../logs/report

scanReport=$(ls $PATHUSER/../ressource/report/)
for file in $scanReport; do
	cat $PATHUSER/../ressource/report/$file >> $PATHUSER/../logs/report
done

echo -e "
-------------------------------
Vulnerabilities
-------------------------------" >> $PATHUSER/../logs/report

comm1=$(ls $PATHUSER/../ressource/vuln/)
for file in $comm1; do
	vulnCount=$(wc -l $PATHUSER/../ressource/vuln/$file)
	echo -e " Vulnerability Found : ${vulnCount}" >> $PATHUSER/../logs/report
	cat $PATHUSER/../ressource/vuln/$file >> $PATHUSER/../logs/report
done

# logs
echo -e "
-------------------------------
Logs
-------------------------------" >> $PATHUSER/../logs/report

tar fczP /var/mail/mail-"`date +"%d-%m-%Y"`".gz /var/mail/mail
rm -rf /var/mail/mail
su -s /bin/bash -c "/usr/sbin/logcheck" logcheck
count=$(($(cat /var/mail/mail | wc -l)-32))
echo -e "Number of suspicious log entries :\n	${count}" >> $PATHUSER/../logs/report

# MOTD
bash $PATHUSER/updateMotd.sh >> $PATHUSER/../logs/report