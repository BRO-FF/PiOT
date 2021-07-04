#!/bin/bash

rm -rf /etc/hostapd/hostapd.conf
rm -rf /etc/dhcp/dhcpd.conf
rm -rf /etc/sysctl.conf
rm -rf /etc/default/isc-dhcp-server
rm -rf /etc/rsyslog.conf
rm -rf /etc/default/dnsmasq
rm -rf /etc/network/interfaces

cp /root/.config/saver/save/file/hostapd.conf /etc/hostapd/
cp /root/.config/saver/save/file/dhcpd.conf /etc/dhcp/
cp /root/.config/saver/save/file/sysctl.conf /etc/
cp /root/.config/saver/save/file/isc-dhcp-server /etc/default/
cp /root/.config/saver/save/file/rsyslog.conf /etc/
cp /root/.config/saver/save/file/dnsmasq /etc/default/
cp /root/.config/saver/save/file/interfaces /etc/network/