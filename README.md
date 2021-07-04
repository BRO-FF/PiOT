# END OF YEAR PROJECT - ESGI - 5SI1

We are four students at the ESGI school
Here is our year-end project
:)

## Intro :
The expansion of IOT raises new security issues as they populate our domestic network
which could be a privileged gateway to penetrate an infrastructure

## Main goals :
The main goals here is to provide an all-in-one solutions to try mitigate security flaws
- Mac address based trust database
- Mac address based inspection
- Firewall filtering
- Defaut password scans
- Network segmentation

## In development
- Safe to keep password
- Mail server to send warning when new device found
- add password flush rules
- inteface graphique
- add rules ssh different port
- scan ip publique (pas shodan)
- ip privee en /16 plutot que /24

## Team
Our awesome team
- Ethan LENGRAND
- Swan SIMION
- Stephane BLOT
- Guillaume BROFFERIO

## Install
cat requirement-apt | xargs apt install -y
pip3 install -r requirement-pip
expect init/init_db.exp

## Install
Run CherryPy :
python3 /opt/projetmaster-master/graph/tut01.py

## ToDo
- Function scan_asset -> display un report sur la webinterface
- Function display_base(device || IP || mac || isUp) -> n=1 [x(n) for x in list_de_tuple]
