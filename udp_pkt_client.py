
# A python script that is a client and from the command line accepts the starting number and total length and sends the correct
# packet to the server and then waits for the received packet. The  client script checks the received packet by the expected
# packet and returns back to the shell the standard success code if it is correct and an error code if not.

import socket
import struct
import argparse

# Constants
DEFAULT_SERVER_IP = "127.0.0.1"
DEFAULT_UDP_PORT_SEND = 33000
#DEFAULT_UDP_PORT_RECEIVE = 00000
COMMAND = 'R'
REPLY_HEADER = '*'
BUFFER_SIZE = 4096  # Adjust as needed, assuming a max reasonable packet size

def main():
    parser = argparse.ArgumentParser(description="UDP client settings.")
    parser.add_argument("starting_number", type=int, help="Starting number for the sequence.")
    parser.add_argument("total_length", type=int, help="Total length of the sequence.")
    parser.add_argument("--server_ip", type=str, default=DEFAULT_SERVER_IP, help=f"IP address of the server. Default is {DEFAULT_SERVER_IP}.")
    parser.add_argument("--port_send", type=int, default=DEFAULT_UDP_PORT_SEND, help=f"Port to send packets. Default is {DEFAULT_UDP_PORT_SEND}.")
 #   parser.add_argument("--port_receive", type=int, default=DEFAULT_UDP_PORT_RECEIVE, help=f"Port to receive packets. Default is {DEFAULT_UDP_PORT_RECEIVE}.")

    args = parser.parse_args()

    start = args.starting_number
    length = args.total_length
    server_ip = args.server_ip
    udp_port_send = args.port_send
  #  udp_port_receive = args.port_receive

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Create the packet
    # 1 char and 2 unsigned integers
    packet = struct.pack('!B',ord(COMMAND)) + struct.pack('!II', start, length)
    
    client_socket.sendto(packet, (server_ip, udp_port_send))

    received_data, server_address = client_socket.recvfrom(BUFFER_SIZE)

    # Check the reply
    if len(received_data) != 1 + 4 * length:
        print("Invalid packet size received!")
        return 1

    reply_header = chr(struct.unpack("!B", received_data[0:1])[0])

    if reply_header != REPLY_HEADER:
        print("Invalid reply header received!")
        return 1

    # Extract numbers and verify
    for i in range(length):
        num = struct.unpack("!I", received_data[1 + i * 4:1 + (i+1) * 4])[0]
        if num != start + i:
            print(f"Expected {start+i} but got {num}")
            return 1

    print(f"Successfully verified the received packet from {server_address}.")
    return 0

if __name__ == "__main__":
    main()
9