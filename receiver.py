import socket
import os
import threading

FORMAT = "utf-8"
# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 12345))
sock.listen(1)

# Wait for a connection
print('Waiting for a connection...')
conn, addr = sock.accept()
print('Connected by', addr)

# Specify the directory to store the received file
directory = 'D:/MMT/ASS!/'  # Replace with your directory
if not os.path.exists(directory):
    os.makedirs(directory)
# Receive the file
filename = conn.recv(10000000000).decode(FORMAT)
print('Receiving', filename)
filename_only = os.path.basename(filename)
print('Filename:', filename_only)
# filepath = os.path.abspath(filename)
try:
    with open(os.path.join(directory, filename_only), 'wb') as f:
        while True:
            data = conn.recv(10000000000)
            if not data:
                break
            f.write(data)
except OSError as e:
    print('Failed to open file:', e)
# Clean up
print('File received')
# print('File received and saved to', filepath)
conn.close()
sock.close()
