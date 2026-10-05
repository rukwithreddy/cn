
import socket
import json

HOST = "127.0.0.1"
PORT = 12347

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("Server waiting for sender...")

conn, addr = server.accept()
print("Connected to:", addr)

expected = 1
lost_frame = False

try:
    with conn:
        stream = conn.makefile("rwb")

        while True:
            line = stream.readline()

            if not line:
                break

            msg = json.loads(line.decode())

            # Handle control messages safely
            if msg["type"] == "end":
                stream.write(b'{"status":"window_done"}\n')
                stream.flush()
                continue

            if msg["type"] == "quit":
                print("\nSender finished transmission.")
                break

            seq = msg["seq"]
            print(f"\nFrame {seq} received")

            # Simulate loss of frame 2 only once
            if seq == 2 and not lost_frame:
                lost_frame = True
                print("Frame 2 lost (simulated)")
                ack = expected

            elif seq == expected:
                print(f"Frame {seq} received correctly")
                expected += 1
                ack = expected

            else:
                print(f"Frame {seq} discarded; expected {expected}")
                ack = expected

            # ACK represents the next expected frame
            response = {"ack": ack}
            stream.write((json.dumps(response) + "\n").encode())
            stream.flush()

            print(f"Sending ACK: {ack}")

finally:
    server.close()
    print("Server closed.")
    