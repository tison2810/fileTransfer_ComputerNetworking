import socket
import os
import threading
import sys

# Set up the sender socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set up the receiver address and port
receiver_address = 'localhost'  # Replace with the receiver's IP address
receiver_port = 9999  # Replace with the receiver's port number

# Connect to the receiver
sender_socket.connect((receiver_address, receiver_port))

file = open("image.png", "rb")
file_size = os.path.getsize("image.png")

sender_socket.send("received_imaged.png".encode())
sender_socket.send(str(file_size).encode())

data = file.read()
sender_socket.sendall(data)
sender_socket(b"<END>")

file.close()
sender_socket.close()


