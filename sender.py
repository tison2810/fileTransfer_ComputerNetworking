import socket
import os
import threading
import sys

# Set up the sender socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set up the receiver address and port
receiver_address = 'localhost'  # Replace with the receiver's IP address
receiver_port = 12345  # Replace with the receiver's port number

# Connect to the receiver
sender_socket.connect((receiver_address, receiver_port))

# Send the file
# if len(sys.argv) < 2:
#     print('Usage: python sender.py <filename>')
#     sys.exit(1)

# filename = sys.argv[1]
# with open(filename, 'rb') as f:
#     data = f.read()
#     sender_socket.sendall(data)
if len(sys.argv) < 2:
    print('Usage: python sender.py <filename>')
    sys.exit(1)

filename = sys.argv[1]
filename_bytes = filename.encode('utf-8')
sender_socket.sendall(filename_bytes)
filesize = os.path.getsize(filename)

with open(filename, 'rb') as f:
    data = f.read()
    sender_socket.sendall(data)


# Close the socket
sender_socket.close()
