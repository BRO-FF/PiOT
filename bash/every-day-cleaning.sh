#!/bin/bash

# Every Day Cleaning
scanZip=$(ls /opt/projetmaster-master/logs/tshark/)
for file in $scanZip; do
	gzip /opt/projetmaster-master/logs/tshark/$file
done

scanZiped=$(ls /opt/projetmaster-master/logs/tshark/)
for file in $scanZiped; do
	mv /opt/projetmaster-master/logs/tshark/$file /opt/projetmaster-master/logs/last-week/$file
done