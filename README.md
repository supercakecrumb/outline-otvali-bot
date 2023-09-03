# otvali-bot

## Deployment

1. копируем на сервер docker-compose.yaml `scp -i ~/.ssh/yc /Users/val-kiel/Personal/frankfurt/vpn-otvali-bot/docker-compose.yaml val-kiel@158.160.119.15:docker-compose.yaml`
2. копируем на сервер `scp -i ~/.ssh/yc /Users/val-kiel/Personal/frankfurt/vpn-otvali-bot/deploy.sh val-kiel@158.160.119.15:deploy.sh`
3. На сервере ./deploy.sh. Должно работать.

Вместо этого можно курлить с репы, но это может не прокатить once it's been made private