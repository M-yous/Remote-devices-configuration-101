# Import required modules/packages/library
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import result
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import session
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import route_pattern
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import prefix_pattern
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import prefix
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import intf_pattern
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-4 import OSPF_pattern
from home.devasc.labs.prne.using-conditionals-with-network-devices-part-2 import routes
import pexpect
from pprint import pprint
import re

# Display heading
print('')
print('Interfaces,   routes list,  routes details')
print('------------------------------------------')

# Create regular expression to match Gigabit interfaces
gig_pattern = re.compile(r'(GigabitEthernet)(\d\/\d\/\d\/d)')

# Create regular expressions to match interfaces and OSPF
OSPF_pattern = re.compile(r'O.+')
intf_pattern = re.compile(r'(GigabitEthernet)(\d)')

# Create regular expression to match prefix and routes
prefix_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/d?\d?)')
route_pattern = re.compile(r'vian(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Create a dictionary to hold the count of routers
# Forwarded out each interface
routes = {}
# Read all lines of IP routing information
file = open('ip-routes.txt', 'r')

# Connect to device and run 'show ip route' command
print('--- connecting telnet 192.168.56.101 with prne/cisco123!')

session1 = pexpect.spawn('telnet 192.168.56.101', encoding='utf-8', timeout=20)
session2 = pexpect.spawn('telnet 192.168.56.130', encoding='utf-8', timeout=20)
result = session1.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

# Check for failure
if result != 0:
    print('Timeout or unexpected replay from device')
    exit()
# Enter username
session.sendline('prne')
result = session.expect('password:')

# Enter password
session.sendline('cisco123!')
result = session.expect('>')
