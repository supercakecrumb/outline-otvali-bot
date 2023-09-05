#!/bin/bash
set -e

BOT_IMAGE=${BOT_IMAGE:-valyankilyan/otvali_bot:0.0.1}
OUTLINE_IMAGE=${OUTLINE_IMAGE:-valyankilyan/outline_service:0.0.1}
USER_WEBHOOK=${USER_WEBHOOK:-False}
POSTGRES_IP=${POSTGRES_IP:-51.250.71.250:5432}

SECRET_ID=${SECRET_ID:-e6qnd7ibmveg2m8pbenp}

IAM_TOKEN=$(curl -H Metadata-Flavor:Google http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token | jq -r .access_token)
SECRET_PAYLOAD=$(curl -X GET -H "Authorization: Bearer ${IAM_TOKEN}" https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/${SECRET_ID}/payload)

BOT_TOKEN=$(echo $SECRET_PAYLOAD | jq -r '.entries[] | select(.key=="BOT_TOKEN") | .textValue')
ADMIN_PASSWORD=$(echo $SECRET_PAYLOAD | jq -r '.entries[] | select(.key=="admin-password") | .textValue')

POSTGRES_USER=$(echo $SECRET_PAYLOAD | jq -r '.entries[] | select(.key=="postgres-user") | .textValue')
POSTGRES_PASSWORD=$(echo $SECRET_PAYLOAD | jq -r '.entries[] | select(.key=="postgres-password") | .textValue')
SQL_ENGINE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_IP}/

docker compose up -d