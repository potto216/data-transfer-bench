#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

#TODO add command line option for TCP/ UDP port number   (default 5555)  (use argparse)


import sys
import re
import zmq

MIN_ARGS = 2
DEFAULT_PORT_NUMBER=5555

def is_valid_ip(ip_address):
    """Check if the given IP address is valid."""
    pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip_address))


if len(sys.argv) < MIN_ARGS:
    print("Usage: python hello_world_client.py <ip_address> <port_number> (optional default 5555))")
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
print(f"Connecting to hello world server on {connection_url}…")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(connection_url)

# Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending request {request} …")
    socket.send(b"Hello")

    # Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")

