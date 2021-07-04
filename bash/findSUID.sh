#!/bin/bash

# Find SUID files
if [ -e /tmp/fichierSUID ]; then
	rm /tmp/fichierSUID
fi

# Parse file
fileSuid="$(find / -type f -user root -perm -u=s -print 2>/dev/null)"
for obj in $fileSuid
do
	echo `ls -l $obj` >> /tmp/fichierSUID
done

# Diff between files
results=$(diff /tmp/fichierSUID $PATHUSER/../ressource/fichierSUID)
if [ -z "$results" ]
then
	echo "---" >> $PATHUSER/../logs/report
	echo "SUID : OK" >> $PATHUSER/../logs/report
	echo "---" >> $PATHUSER/../logs/report
else
	echo "---" >> $PATHUSER/../logs/report
	echo "SUID file modified" >> $PATHUSER/../logs/report
	echo "---" >> $PATHUSER/../logs/report
	echo $results >> $PATHUSER/../logs/report
fi