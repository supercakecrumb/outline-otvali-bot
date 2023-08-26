# VPN manager

This will be a service that will be running inside vpn server machine and manage users. It will generate configurations, secrets and users. Then it will upload it to s3 in YC. Also it needs to have endpoint for creating new users with some kind of authorization. Data will be sent via gRPC protocol.