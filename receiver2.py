import socket
import tqdm

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind(("localhost", 9999))
receiver_socket.listen()

sender_socket, address = receiver_socket.accept()

file_name = sender_socket.recv(1024).decode()
print(file_name)
file_size = sender_socket.recv(1024).decode()
print(file_size)
file = open(file_name, "wb")

file_bytes = b""

done = False

progess = tqdm.tqdm(unit="B",unit_scale=True, unit_divisor=1000,total=int(file_size))
while not done:
    data = sender_socket.recv(1024)
    if file_bytes[-5:] == b"<END":
        done = True
    else: 
        file_bytes += data
    progess.update(1024)
file.write(file_bytes)

file.close()
sender_socket.close()
receiver_socket.close()