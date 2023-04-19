#!/bin/bash

# Crear Security Group para servidores en DMZ
openstack security group create DMZ-SG
# Habilitar acceso via SSH
openstack security group rule create --protocol tcp --ingress --dst-port 22 DMZ-SG
# Habilitar acceso web
openstack security group rule create --protocol tcp --ingress --dst-port 80 DMZ-SG
# Habilitar acceso SNMP  desde servidor Nagios
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 161 --ingress DMZ-SG
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 162 --ingress DMZ-SG

# Crear Security Group para database
openstack security group create Database-SG
# Habilitar acceso Postgresql
openstack security group rule create --ethertype IPv4 --protocol tcp --remote-ip 10.0.10.10/32 --dst-port 5432 --ingress Database-SG
# Habilitar acceso via SSH
openstack security group rule create --ethertype IPv4 --protocol tcp --remote-ip 10.0.0.0/16 --dst-port 22 --ingress Database-SG
# Habilitar acceso SNMP  desde servidor Nagios
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 161 --ingress Database-SG
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 162 --ingress Database-SG

# Crear Security Group para ansible, nagios
openstack security group create Ansible-SG
# Habilitar acceso via SSH
openstack security group rule create --ethertype IPv4 --protocol tcp --remote-ip 10.0.0.0/16 --dst-port 22 --ingress AnsibleNagios-SG
# Habilitar acceso SNMP  desde servidor Nagios
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 161 --ingress AnsibleNagios-SG
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 162 --ingress AnsibleNagios-SG

# Crear Security Group para elk
openstack security group create Ansible-SG
# Habilitar acceso via SSH
openstack security group rule create --ethertype IPv4 --protocol tcp --remote-ip 10.0.0.0/16 --dst-port 22 --ingress ELK-SG
# Habilitar acceso SNMP  desde servidor Nagios
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 161 --ingress ELK-SG
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.20.0/24 --dst-port 162 --ingress ELK-SG
# Habilitar puertos Elasticsearch, Logstash (UDP)
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.0.0/16 --dst-port 9200 --ingress ELK-SG
openstack security group rule create --ethertype IPv4 --protocol udp --remote-ip 10.0.10.10/32 --dst-port 5000 --ingress ELK-SG


# Crear floating IP para servidor en DMZ (webserver, grafana)
openstack floating ip create --project $project --floating-ip-address 192.168.200.219 provider
openstack floating ip create --project $project --floating-ip-address 192.168.200.220 provider

# Asociar FIP a WebServer, Grafana
openstack server add floating ip webserver 192.168.200.219
openstack server add floating ip grafana 192.168.200.220


