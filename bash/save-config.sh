#!/bin/bash

#	Save PA
#	-
#	30 05 * * * /opt/projetmaster-master/bash/save-config.sh
#	
if [[ ! -d "/root/.config/saver/" ]]; then
	mkdir -p /root/.config/saver/save
else
	rm -rf /root/.config/saver/save/*
fi

#	Export dir
cp -R /opt/ /root/.config/saver/save
cp -R /root/.config/cheat/ /root/.config/saver/save/file/

#	Export conf file
cp /etc/hostapd/hostapd.conf /root/.config/saver/save/file/
cp /etc/dhcp/dhcpd.conf /root/.config/saver/save/file/
cp /etc/sysctl.conf /root/.config/saver/save/file/
cp /etc/default/isc-dhcp-server /root/.config/saver/save/file/
cp /etc/rsyslog.conf /root/.config/saver/save/file/
cp /etc/default/dnsmasq /root/.config/saver/save/file/
cp /etc/network/interfaces /root/.config/saver/save/file/
cp /lib/ipSave/rulesIPtables /root/.config/saver/save/file/

# Export DB
mysqldump -u root -ptoor --all-databases > /root/.config/saver/save/dump.sql

tar fczP /root/.config/saver/save-"`date +"%d-%m-%Y"`".gz /root/.config/saver/save