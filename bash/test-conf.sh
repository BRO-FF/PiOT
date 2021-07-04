#!/bin/bash
mkdir /opt/projetmaster-master/ressource/json
mkdir /opt/projetmaster-master/ressource/vuln
chown -R cherrypy:cherrypy /opt/projetmaster-master/
chmod -R 751 /opt/projetmaster-master/
# /usr/bin/python3 /opt/projetmaster-master/ip/scan-asset.py
# /opt/projetmaster-master/bash/runManage.sh
# /usr/bin/python3 /opt/projetmaster-master/ip/sendMail.py