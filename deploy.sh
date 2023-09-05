#!/bin/bash

if ! [[ -f .env ]]; then
    echo "Error: .env file not found. Create it from dotenv_example"
    exit 1
fi

SERVER_IP_ADDRESS=${SERVER_IP_ADDRESS:-"51.250.71.250"}
REMOTE_DIR=${REMOTE_DIR:-"/var/otvali"}
SSH_USER=${SSH_USER:-"val-kiel"}
SSH_KEY=${SSH_KEY:-"~/.ssh/yc"}


ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" << 'ENDSSH'
  if [ ! -d "/var/otvali" ]; then
    sudo mkdir -p /var/otvali
    sudo groupadd -f otvali
    USERNAME=$(whoami)
    sudo usermod -aG otvali $USERNAME
    sudo chown :otvali /var/otvali
    sudo chmod 770 /var/otvali
  fi
ENDSSH

FILES=(".env" "docker_compose_up.sh" "docker-compose.yaml")

for FILE in "${FILES[@]}"; do
  scp -i "${SSH_KEY}" "$FILE" "${SSH_USER}@${SERVER_IP_ADDRESS}:${REMOTE_DIR}/"
done


ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" "bash ${REMOTE_DIR}/docker_compose_up.sh"
