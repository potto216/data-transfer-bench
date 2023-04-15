import subprocess
import argparse
import re
import zmq

# program sends a command to the server and the server executes the command and sends the output back to the client

support_commands = ["run","dir","ls"]
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
    parser.add_argument("--port", "-p", type=int, default=5555, help="TCP/UDP port number (default: 5555)")

    args = parser.parse_args()
    ip_address = args.ipv4
    port_number = args.port

    
    print(f"Validated input: IP address = {ip_address}, port = {port_number}")
    print(f"The supported commands are {support_commands}")
    
    # Socket to talk to server
    connection_url = f"tcp://{ip_address}:{port_number}"
    print(f"Waiting for command on {connection_url}…")
    context = zmq.Context()   
    socket = context.socket(zmq.REP)
    socket.bind(connection_url)

    #  Wait for next request from client
    message = socket.recv()
    print(f"Received message {message}")
    
    command = message.decode("utf-8")
    # test if message is a valid command
    if command in support_commands:
        run_command(ip_address, command)
    else:
        print(f"Invalid command of {command}")
    
    print("Exiting…")


if __name__ == "__main__":
    main()

def run_command(ipv4, command):
    # The command to run (replace 'ls' with your desired command)
    if command is None:
        command = "ls" # default command 

    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"An error occurred while executing the command {command}:\n{stderr}")
    else:
        print(f"Command output:\n{stdout}")
