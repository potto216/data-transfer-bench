#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import sys
import re

MIN_ARGS = 2
DEFAULT_PORT_NUMBER=5555

def is_valid_ip(ip_address):
    """Check if the given IP address is valid."""
    pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip_address))

if len(sys.argv) < MIN_ARGS:
    print("Usage: python hello_world_server.py <ip_address> <port_number> (optional default 5555))")
    sys.exit(1)

ip_address = sys.argv[1]
if not is_valid_ip(ip_address):
    print("Invalid IP address format. Please provide a valid IP address.")
    sys.exit(1)

if len(sys.argv) > MIN_ARGS: # port number is provided
    port_number = sys.argv[2]
    if not port_number.isdigit():
        print("Invalid port number format. Please provide a valid port number.")
        sys.exit(1)
    port_number = int(port_number)
else:
    port_number = DEFAULT_PORT_NUMBER

# Socket to talk to server
connection_url = f"tcp://{ip_address}:{port_number}"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(connection_url)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
