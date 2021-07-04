#!/bin/bash
host_up_config() {
	# CRONTAB
	crontab -l > /lib/ipSave/mycron
	echo -e "*/5 * * * * /usr/bin/python3 /opt/projetmaster-master/mac/hostup.py" >> /lib/ipSave/mycron
	crontab /lib/ipSave/mycron
	rm /lib/ipSave/mycron

}
host_up_config