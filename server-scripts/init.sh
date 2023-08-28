#!/bin/bash
set -ex

sudo add-apt-repository ppa:certbot/certbot

sudo apt update -y
sudo apt upgrade -y

sudo apt install strongswan strongswan-pki
sudo apt install software-properties-common certbot


# probably on server
# export SERVER_DOMAIN=frankfurt-test.vkiel.com
# export VPN_SERVER_IP="192.168.1.1"
# export VPN_SERVER_CERT_PATH="/etc/ipsec.d/certs/server.crt"

# Create certificate for server domain
sudo certbot certonly --standalone -d ${SERVER_DOMAIN}

# Edit configuration and move it in place
envsubst < files/ipsec.conf.tpl > files/ipsec.conf
sudo mv files/ipsec.conf /etc/ipsec.conf

# Create root certificate authority for client certificates 
openssl genpkey -algorithm RSA -out ca-key.pem
openssl req -new -x509 -days 36500 -key ca-key.pem -out ca-cert.pem

# Move the CA files
sudo mv ca-key.pem /etc/ipsec.d/private/
sudo mv ca-cert.pem /etc/ipsec.d/cacerts/

# Update permissions to ensure StrongSwan can read them
sudo chmod 600 /etc/ipsec.d/private/ca-key.pem
sudo chmod 644 /etc/ipsec.d/cacerts/ca-cert.pem


# Then in order to create client certificate 
# openssl genpkey -algorithm RSA -out client-key.pem
# openssl req -new -key client-key.pem -out client-csr.pem
# openssl x509 -req -days 3650 -in client-csr.pem -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem





