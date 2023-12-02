# Import required modules/packages/library
import pexpect
from pprint import pprint
import re
# Display heading
print('')
print('Interfaces, routes list, routes details')
print('---------------------------------------')

# Create regular expressions to match interfaces and OSPF
OSPF_pattern = re.compile(r'O.+')
intf_pattern = re.compile(r'(GigabitEthernet)(\d)')

# Create regular expressions to match prefix and routes
prefix_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/?\d?\d?)')
route_pattern = re.compile(r'via (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Connect to device and run 'show ip route' command
print('--- connecting telnet 192.168.56.101 with prne/cisco123!')
print('--- connecting telnet 192.168.56.130 with prne/cisco123!')
session1 = pexpect.spawn('telnet 192.168.56.101', encoding='utf-8', timeout=20)
result1 = session1.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])
session2 = pexpect.spawn('telnet 192.168.56.130', encoding='utf-8', timeout=20)
result2 = session2.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

# Check for failure
if result1 != 0:
    print('Timeout or unexpected reply from device')
    exit()
if result2 != 0:
    print('Timeout or unexpected reply from device')    
# Enter username
session1.sendline('prne')
result1 = session1.expect('Password:')
session2.sendline('prne')
result2 = session2.expect('password')

# Enter password
session1.sendline('cisco123!')
result1 = session1.expect('>')
session2.sendline('cisco123!')
result2 = session2.expect('>')

# Must set terminal length to zero for long replies, no pauses
print('--- setting terminal length to 0')
session1.sendline('terminal length 0')
result1 = session1.expect('>')
session2.sendline('terminal length 0')
result2 = session2.expect('>')
# Run the 'show ip route' command on device
print('--- successfully logged into device, running show ip route command')
session1.sendline('show ip route')
result1 = session1.expect('>')
session2.sendline('show ip route')
result2 = session2.expect('>')
# Display the output of the command, for comparison
print('--- show ip route output:')
show_ip_route_output1 = session1.before
print(show_ip_route_output1)
show_ip_route_output2 = session2.before
print(show_ip_route_output2)
# Get the output from the command into a list of lines from the output
routes_list1 = show_ip_route_output1.splitlines()
routes_list2 = show_ip_route_output2.splitlines()
# Create dictionary to hold number of routes per interface
intf_routes = {}

# Go through the list of routes to get routes per interface
for route in  routes_list1:

    OSPF_match = OSPF_pattern.search(route)
    if OSPF_match:

        # Match for GigabitEthernet interfaces
        intf_match = intf_pattern.search(route) 
        
        # Check to see if we matched the GigabitEthernet interfaces string
        if intf_match:

            # Get the interfaces from the match
            intf = intf_match.group(2)

            # If route list not yet created, do so now
            if intf not in intf_routes:
                intf_routes[intf] = []

                # Exract the prefix (destination IP address/subnet)
            prefix_match = prefix_pattern.search(route)
            prefix = prefix_match.group(1)

                # Extract the route
            route_match = route_pattern.search(route)
            next_hop = route_match.group(1)

                # Create dictionary for this this route,
                # and add it to the list
            route = {'prefix': prefix, 'next-hop': next_hop}
            intf_routes[intf].append(route)

for route in  routes_list2:

    OSPF_match = OSPF_pattern.search(route)
    if OSPF_match:

        # Match for GigabitEthernet interfaces
        intf_match = intf_pattern.search(route) 
        
        # Check to see if we matched the GigabitEthernet interfaces string
        if intf_match:

            # Get the interfaces from the match
            intf = intf_match.group(2)

            # If route list not yet created, do so now
            if intf not in intf_routes:
                intf_routes[intf] = []

                # Exract the prefix (destination IP address/subnet)
            prefix_match = prefix_pattern.search(route)
            prefix = prefix_match.group(1)

                # Extract the route
            route_match = route_pattern.search(route)
            next_hop = route_match.group(1)

                # Create dictionary for this this route,
                # and add it to the list
            route = {'prefix': prefix, 'next-hop': next_hop}
            intf_routes[intf].append(route)             


# Display a blank line to make easier to read
print('')

# Display a title
print('OSPF routes out of GigabitEthernet interfaces:')

# Display the GigabitEthernet interfaces routes
pprint(intf_routes)

# Display a blank line to make easier to read
print('')
# Close the file
#file.close()
