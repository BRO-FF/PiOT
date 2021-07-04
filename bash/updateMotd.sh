#!/bin/sh

lan=$(ip a | sed -n 7p | cut -d ' ' -f6)
wlan=$(ip a | sed -n 11p | cut -d ' ' -f6)

echo "-------------------------------"
echo Updates
echo "-------------------------------"
echo -e "Number of outdated package :"
apt list --upgradable 2>/dev/null | wc -l
echo "-------------------------------"
echo Network
echo "-------------------------------"
echo "- LAN = "$lan
echo "- WLAN = "$wlan
echo "- WAN = "$(curl ifconfig.io 2>/dev/null)
echo "-------------------------------"
echo System
echo "-------------------------------"
echo "- Version OS =" $(head -1 /etc/os-release | awk '{split($0,a,"="); print a[2]}')
echo "- Uptime = "$(uptime | awk '{print $3,$4}' | cut -d ',' -f1)
echo "- Kernel = "$(uname -r)
echo "- Utilisateurs =" $(uptime | cut -d ' ' -f7)
echo "-------------------------------"
echo Memory
echo "-------------------------------"
echo "- Total memory = " $(free -m | grep Mem: | awk '{print $2}') "Mb"
echo "- Used memory =" $(free -m | grep Mem: | awk '{print $3}') "Mb"
echo "- Available memory = " $(free -m | grep Mem: | awk '{print $7}') "Mb"
echo "- Free memory = " $(free -m | grep Mem: | awk '{print $4}') "Mb"
echo "==============================="