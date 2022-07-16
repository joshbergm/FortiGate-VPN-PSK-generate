from netmiko import ConnectHandler
import random
import string
import time

#Specify connection details
remote_fortigate = { 'host': '<remote_hostname>',
      'device_type': 'fortinet',
      'ip': '<IP>',
      'username': '<user>',
      'password': '<password>' }

local_fortigate = { 'host': '<local_hostname>',
      'device_type': 'fortinet',
      'ip': '<ip>',
      'username': '<username>',
      'password': '<password>' }

#Generate PSK
def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in
    range(length))

VPN_PSK = generate_key(16)

#Generate command set
REMOTE_COMMANDS = ['config vpn ipsec phase1-interface',
                      'edit "<VPN NAME>"',
                      'set psk ' + VPN_PSK]

LOCAL_COMMANDS = ['config vpn ipsec phase1-interface',
                     'edit "<VPN NAME>"',
                     'set psk ' + VPN_PSK]

#Start SSH connection (remote, local)
SSH_REMOTE_FORTIGATE = ConnectHandler(**remote_fortigate)
SSH_LOCAL_FORTIGATE = ConnectHandler(**local_fortigate)

#Send SSH commands (remote, local)
SSH_REMOTE_FORTIGATE.send_config_set(REMOTE_COMMANDS)
time.sleep(5)
SSH_LOCAL_FORTIGATE.send_config_set(LOCAL_COMMANDS)

#Stop SSH connection (remote, local)
SSH_REMOTE_FORTIGATE.disconnect()
SSH_LOCAL_FORTIGATE.disconnect()
