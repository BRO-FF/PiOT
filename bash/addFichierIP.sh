#!/bin/bash
# SUID
files="$(find / -type f -user root -perm -u=s -print 2>/dev/null)"
for obj in $files
do
	echo `ls -l $obj` >> /opt/projetmaster-master/ressource/fichierSUID
done

#	IP
grep -oP --exclude='lastlog' --exclude='dpkg*' '([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])' /var/log/*log* 2>/dev/null | cut -d ":" -f 2 | sort -u > /opt/projetmaster-master/ressource/fichierIP