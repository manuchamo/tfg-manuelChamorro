#!/bin/bash

## Creación de imagenes
openstack image create --file kinetic-server-cloudimg-amd64-disk-kvm.img --disk-format qcow2 --min-disk 20 --min-ram 1024 --no-share ubuntu_22.10
openstack image create --file CentOS-7-x86_64-Minimal.img --disk-format qcow2 --min-disk 15 --min-ram 512 --no-share centos


## Creacion de flavors 
openstack flavor create --ram 1024 --disk 20 --vcpus 2 medium.flavor
openstack flavor create --ram 512 --disk 15 --vcpus 1 small.flavor