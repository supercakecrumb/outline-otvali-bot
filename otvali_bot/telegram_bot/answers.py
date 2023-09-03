from .types import get_key_command

help_text = '''
*OtVali HowTo*

1. Approval:
   - Wait for admin approval to gain access to our servers. You will be notified once approved.

2. Get key:
   - Choose a server and get your special key to access the server with the command `/get_key`.

3. Insert:
   - Insert it in your shadowsocks application of your choice.

*Clients*

If you don't know where to install the VPN client, you could choose from here:
- [outlineVPN](https://clck.ru/35Zeh9) (for every platform)
- [TrueNight](https://clck.ru/35ZehW) (for android)
'''


already_approved_text = f"Your request already has been approved. In order to get VPN credentials write /{get_key_command}"
already_requested_text = "You already requested VPN credentials. We will notify you as soon as answers approves your request"
request_declined_text = "Sorry, but your request was declined"
request_waitlist_text = "Your request has been sent to the admin, wait for the approvement"
