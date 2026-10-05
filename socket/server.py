
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 12345))
server.listen(5)

print("Server is waiting for a client...")

while True:
    conn, addr = server.accept()
    print("Connected to:", addr)

    while True:
        data = conn.recv(1024)

        if not data:
            break

        message = data.decode()
        print("Client:", message)

        conn.sendall(data)

    conn.close()
    print("Client disconnected")

