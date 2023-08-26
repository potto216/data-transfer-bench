# A simple python script that is a udp server. The script will wait for a packet request on udp port  33000. The packet payload will be 9 bytes. 
# The first byte is a command and the only valid option is the ascii 'R'. The next 4 bytes is an unsigned integer representing a starting number.
# The final 4 bytes is another unsigned integer representing a length. When the server receives this payload and decodes it the server will send
# a reply on udp port 33001 that is a payload with the first byte the ascii '*' and the rest of the  of the payload composed of 4 byte unsigned
# integers in an ascending counting sequence incrementing by 1. The integers will start at the received starting number and the total number
# of integers is the received length. After sending this packet the server will wait for the next packet and repeat the process.


import socket
import struct
import argparse

# Constants
DEFAULT_UDP_IP = "0.0.0.0"
DEFAULT_UDP_PORT_RECEIVE = 33000
DEFAULT_UDP_PORT_SEND = 33001
BUFFER_SIZE = 9
COMMAND = 'R'
REPLY_HEADER = '*'
PACKET_FORMAT = "!BII"

def main():
    parser = argparse.ArgumentParser(description="UDP server settings.")
    parser.add_argument("--ip", type=str, default=DEFAULT_UDP_IP, help=f"IP address to bind the server. Default is {DEFAULT_UDP_IP}.")
    parser.add_argument("--port_receive", type=int, default=DEFAULT_UDP_PORT_RECEIVE, help=f"Port to receive packets. Default is {DEFAULT_UDP_PORT_RECEIVE}.")
    parser.add_argument("--port_send", type=int, default=DEFAULT_UDP_PORT_SEND, help=f"Port to send packets. Default is {DEFAULT_UDP_PORT_SEND}.")

    args = parser.parse_args()

    udp_ip = args.ip
    udp_port_receive = args.port_receive
    udp_port_send = args.port_send

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port_receive))
    print(f"Listening on {udp_ip}:{udp_port_receive}...")

    while True:
        data, client_address = sock.recvfrom(BUFFER_SIZE)
        if len(data) != BUFFER_SIZE:
            continue

        cmd, start, length = struct.unpack(PACKET_FORMAT, data)

        if chr(cmd) == COMMAND:
            reply_payload = [struct.pack("!B", ord(REPLY_HEADER))]
            for i in range(start, start+length):
                reply_payload.append(struct.pack("!I", i))

            response = b"".join(reply_payload)
            #sock.sendto(response, (addr[0], udp_port_send))
            #print(f"Sent reply to {addr[0]}:{udp_port_send}")
            sock.sendto(response,client_address)
            print(f"Sent reply to {client_address}")

if __name__ == "__main__":
    main()
