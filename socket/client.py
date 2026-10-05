
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 12345))

print("Connected to server.")
print("Type 'exit' to disconnect.")

while True:
    message = input("Enter message: ")

    if message.lower() == "exit":
        break

    client.sendall(message.encode())

    data = client.recv(1024)
    print("Echo from server:", data.decode())

client.close()
print("Disconnected from server.")
