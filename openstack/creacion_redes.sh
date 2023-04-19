#!/bin/bash

# Datos de proyecto: nombre, descripcion
project="Entorno_TFG"
description="Proyecto Entorno_TFG"

# Datos de usuario que crearemos para administrar el proyecto: nombre, correo, contrasena
usuario="manuel"
correo="manuel.chamorrom@estudiante.uam.es"
user_password="vbwrhjtuksdfv4#"

# Datos para la creacion de la red provider/red externa 
declare -A redExterna
redExterna=( ["name"]="provider" ["network"]="192.168.1.0/24" ["gateway"]="192.168.1.1" ["start-allocation"]="192.168.1.213" ["end-allocation"]="192.168.1.220" )

# Datos para la creacion de la red DMZ
declare -A redDmz
redDmz=( ["name"]="dmz-network" ["network"]="10.0.10.0/24" ["gateway"]="10.0.10.254" )

# Datos para la creacion de la red interna
declare -A redInterna
redInterna=( ["name"]="internal-LAN-network" ["network"]="10.0.20.0/24" )

# Datos para la creacion del router para trafico Norte-Sur
declare -A routerNS
routerNS=( ["name"]="public-router" )

# Datos para la creacion del router para trafico Este-Oeste
declare -A routerEW
routerEW=( ["name"]="dmz-internal-router" )

# Crear Proyecto 
openstack project create --description $description $project

# Crear usuario y asignar permisos sobre el proyecto 
openstack user create --password $user_password --email $correo  --project $project $usuario
openstack role add --user $usuario --project $project admin
openstack role add --user $usuario --project $project Member

# Crear red provider (no asignada a proyecto)
openstack network create --share --enable --external --provider-network-type flat --provider-physical-network extnet ${redExterna[name]}

# Crear red DMZ (red tenant)
openstack network create --no-share --enable --project $project --internal ${redDmz[name]}

# Crear red interna LAN (red tenant)
openstack network create --no-share --enable --project $project --internal ${redInterna[name]}

# Creacion de subred provider (sin DHCP)
openstack subnet create --project $project --subnet-range ${redExterna[network]} --gateway ${redExterna[gateway]} --network ${redExterna[name]} --allocation-pool start=${redExterna[start-allocation]},end=${redExterna[end-allocation]} --no-dhcp  public-subnet

# Creacion de subred DMZ (habilitamos el DHCP para asignar IP de red)
openstack subnet create --project $project --subnet-range ${redDmz[network]} --host-route destination=${redInterna[network]},gateway=${redDmz[gateway]} --network ${redDmz[name]} --dhcp  dmz-subnet

# Creacion de subred interna (con DHCP habilitado)
openstack subnet create --project $project --subnet-range ${redInterna[network]} --network ${redInterna[name]} --dhcp  internal-subnet

# Creacion de routers para conectividad entre subredes
openstack router create --project $project --enable ${routerNS[name]}
openstack router create --project $project --enable ${routerEW[name]}

# Conectividad con red provider
openstack router set --enable --external-gateway ${redExterna[name]} --enable-snat ${routerNS[name]}
openstack router add subnet ${routerNS[name]} dmz-subnet 

# Conectividad entre subred de DMZ, subred LAN.
# IMPORTANTE: Asignar IP de interfaz para permitir la creacion de tabla de rutas (IP 10.0.10.254)
openstack router add subnet ${routerEW[name]} internal-subnet 
openstack router add subnet ${routerEW[name]} dmz-subnet 