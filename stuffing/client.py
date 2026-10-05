
import socket

HOST = "127.0.0.1"
PORT = 12349

FLAG = "F"
ESC = "E"

data = input("Enter data: ")

# Perform byte stuffing
stuffed_data = ""

for ch in data:
    if ch == FLAG or ch == ESC:
        stuffed_data += ESC

    stuffed_data += ch

# Add FLAG characters at both ends
frame = FLAG + stuffed_data + FLAG

print("Original data:", data)
print("Stuffed data:", stuffed_data)
print("Transmitted frame:", frame)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
    client.sendall(frame.encode())
    print("Frame sent successfully.")

finally:
    client.close()
    