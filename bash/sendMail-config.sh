#!/bin/bash
sendMailConfig() {
	# CRONTAB
	crontab -l > /lib/ipSave/mycron
	echo -e "15 03 * * * /usr/bin/python3 /opt/projetmaster-master/ip/scan_asset.py" >> /lib/ipSave/mycron
	echo -e "30 05 * * * /opt/projetmaster-master/bash/runManage.sh" >> /lib/ipSave/mycron
	echo -e "15 08 * * * /usr/bin/python3 /opt/projetmaster-master/ip/sendMail.py" >> /lib/ipSave/mycron
	crontab /lib/ipSave/mycron
	rm /lib/ipSave/mycron

}
sendMailConfig