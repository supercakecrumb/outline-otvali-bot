# /etc/ipsec.conf
config setup
    charondebug="ike 2, knl 2, cfg 2, net 2, esp 2, dmn 2,  mgr 2"

conn %default
    keyexchange=ikev2
    ike=aes256-sha1-modp1024!
    esp=aes256-sha1!
    dpdaction=clear
    dpddelay=300s

conn myvpn
    right=${SERVER_DOMAIN}
    rightcert=${VPN_SERVER_CERT_PATH}
    rightsubnet=0.0.0.0/0
    rightdns=8.8.8.8
    leftsourceip=%config
    auto=add