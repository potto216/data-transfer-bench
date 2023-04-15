import subprocess
import argparse
import re
import zmq

# program sends a command to the server and the server executes the command and sends the output back to the client

def is_valid_ip(ip_address):
    """Check if the given IP address is valid."""
    pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip_address))

def valid_ipv4(ipv4):
    if not is_valid_ip(ipv4):
        raise argparse.ArgumentTypeError("Invalid IPv4 address")
    return ipv4

def main():
    parser = argparse.ArgumentParser(description="A simple program to validate IPv4 address and command")
    
    parser.add_argument("ipv4", type=valid_ipv4, help="IPv4 address")
    parser.add_argument("command", choices=["run","ls","dir"], help="Command to execute")
    parser.add_argument("--port", "-p", type=int, default=5555, help="TCP/UDP port number (default: 5555)")

    args = parser.parse_args()
    ip_address = args.ipv4
    port_number = args.port
    command = args.command
    
    print(f"Validated input: IP address = {ip_address}, port = {port_number}, command = {command}")
    
    # Socket to talk to server
    connection_url = f"tcp://{ip_address}:{port_number}"
    print(f"Connecting to hello world server on {connection_url}…")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(connection_url)

    print(f"Sending command: {command}")
    socket.send_string(command)

if __name__ == "__main__":
    main()
