#!/bin/bash

# Var
read -e -p "Enter hostname : " hostName
read -e -p "Enter domain name : " domainName
read -e -p "Enter your ip : " ipUser
read -e -p "Enter your mask : " maskUser

ip3=$(echo $ipUser | awk '{split($0,a,"."); print a[3]}')
ip1=$(echo $ipUser | awk '{split($0,a,"."); print a[1]}')
ip2=$(echo $ipUser | awk '{split($0,a,"."); print a[2]}')
ip4=$(echo $ipUser | awk '{split($0,a,"."); print a[4]}')

networkUser="$ip1.$ip2.$ip3.0/$maskUser"


# Conf hostname
echo -e "$hostName.$domainName" > /etc/hostname

systemctl restart named
#	/etc/bind/named.conf.options
echo -e "
acl \"trusted\" {
	$ipUser;
	$ip1.$ip2.$ip3.1;
	};

options {
	directory \"/var/cache/bind\";
	dnssec-validation auto;
	recursion yes;
	allow-recursion { trusted; };
	listen-on { $ipUser; };
	allow-transfer { none; };

	forwarders {
		8.8.8.8;
		8.8.4.4;
	};
};" > /etc/bind/named.conf.options

#	/etc/bind/named.conf.local
echo -e "
zone \"$domainName\" IN {
	type master;
	file \"/etc/bind/db.$domainName\";
	allow-query { any; };
	allow-transfer { $ip1.$ip2.$ip3.1; };
};

zone \"168.192.in-addr.arpa\" IN {
	type master;
	file \"/etc/bind/db.192.168\";
	allow-transfer { $ip1.$ip2.$ip3.1; };
};" > /etc/bind/named.conf.local

#	/etc/bind/db.$domainName
echo -e "\$TTL	86400
@		IN	SOA	ns1.$domainName. root.$domainName. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			  86400 )	; Negative Cache TTL
;
@		IN	NS	ns1.$domainName.
ns1.$domainName.	IN	A	$ipUser
$hostName.$domainName.	IN	A	$ipUser" > /etc/bind/db.$domainName

# /etc/bind/db.192.168
echo -e "\$TTL	604800
@	IN	SOA	ns1.$domainName. root.$domainName. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	ns1.$domainName.
@	IN	NS	$hostName.$domainName." > /etc/bind/db.$ip1.$ip2

systemctl restart named