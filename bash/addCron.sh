#!/bin/bash
00 00 * * * /usr/bin/python3 /opt/projetmaster-master/ip/cleaning.py
30 05 * * * /opt/projetmaster-master/bash/save-config.sh
15 08 * * * /usr/bin/python3 /opt/projetmaster-master/ip/sendMail.py
*/5 * * * * /usr/bin/python3 /opt/projetmaster-master/mac/hostup.py
0 * * * * /usr/bin/python3 /opt/projetmaster-master/ip/scan_asset.py
5 * * * * /usr/bin/python3 /opt/projetmaster-master/ip/scan_asset_network.py
30 * * * * /opt/projetmaster-master/bash/runManage.sh