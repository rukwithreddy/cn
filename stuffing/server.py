
import socket

HOST = "127.0.0.1"
PORT = 12349

FLAG = "F"
ESC = "E"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("Server waiting for client...")

try:
    conn, addr = server.accept()
    print("Connected to:", addr)

    with conn:
        framed_data = conn.recv(4096).decode()
        print("Received frame:", framed_data)

        if (len(framed_data) < 2
                or framed_data[0] != FLAG
                or framed_data[-1] != FLAG):
            print("Invalid frame")
        else:
            # Remove starting and ending FLAG
            stuffed_data = framed_data[1:-1]

            # De-stuff the data
            original = ""
            i = 0

            while i < len(stuffed_data):
                if stuffed_data[i] == ESC:
                    i += 1

                    if i >= len(stuffed_data):
                        raise ValueError("Invalid escape sequence")

                    original += stuffed_data[i]
                else:
                    original += stuffed_data[i]

                i += 1

            print("De-stuffed data:", original)

finally:
    server.close()
    print("Server closed.")
    