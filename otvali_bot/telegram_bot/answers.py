from .types import get_key_command

help_text = '''
🛡️ *OtVali Help* 🛡️

1. `Approval`
   - Wait for admin approval to gain access to our servers. You will be notified once approved.

2. `/server_list` 
   - Browse through a list of available servers to find one that suits your needs.

3. `/create_key <server>` e.g. /create_key Frankfurt
   - Generate a new access key for the server specified. Use server ID, city, or country as the parameter.

4. `/get_key <server>` e.g. /get_key Germany
   - Retrieve your generated key for immediate use. The message containing the key will be deleted after 1 minute for security.

5. `/my_keys`
   - View a list of servers for which you have an access key.

📌 *Note*: In future updates, you will need admin approval to access individual servers.

Guides for computers: https://centixkadon.github.io/b/app/shadowsocks/client/
Guides for phones: https://play.google.com/store/apps/details?id=de.blinkt.openvpn 
'''

already_approved_text = f"Your request already has been approved. In order to get VPN credentials write /{get_key_command}"
already_requested_text = "You already requested VPN credentials. We will notify you as soon as answers approves your request"
request_declined_text = "Sorry, but your request was declined"
request_waitlist_text = "Your request has been sent to the admin, wait for the approvement"
