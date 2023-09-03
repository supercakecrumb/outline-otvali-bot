#!/bin/bash
set -ex 

IAM_TOKEN=$(curl -H Metadata-Flavor:Google http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token | jq -r .access_token)


BOT_TOKEN=(curl -X GET -H "Authorization: Bearer ${IAM_TOKEN}" https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/e6qgn6al4fc7r4if5r8a/payload | jq -r '.entries[] | select(.key=="bot-token") | .textValue')
ADMIN_PASSWORD=$(curl -X GET -H "Authorization: Bearer ${IAM_TOKEN}" https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/e6qgn6al4fc7r4if5r8a/payload | jq -r '.entries[] | select(.key=="admin-password") | .textValue')