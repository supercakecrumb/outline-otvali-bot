## StrongSwan Configuration

```
export VPN_SERVER_IP="192.168.1.1"
export VPN_SERVER_CERT_PATH="/etc/ipsec.d/certs/server.crt"

envsubst < /path/to/template.ipsec.conf > /etc/ipsec.conf
```