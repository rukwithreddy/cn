
import socket
import json

HOST = "127.0.0.1"
PORT = 12347

total = int(input("Enter total number of frames: "))
window = int(input("Enter window size: "))

if total <= 0 or window <= 0:
    raise ValueError("Frames and window size must be positive.")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stream = client.makefile("rwb")

base = 1

try:
    while base <= total:
        end = min(base + window - 1, total)

        print(f"\nWindow: Frames {base} to {end}")

        # Send all frames in the current window
        for seq in range(base, end + 1):
            print(f"Sending Frame {seq}")

            msg = {"type": "frame", "seq": seq}
            stream.write((json.dumps(msg) + "\n").encode())

        # Tell the server this window has been sent
        stream.write(b'{"type":"end"}\n')
        stream.flush()

        # Receive one ACK for each transmitted frame
        next_expected = base

        for _ in range(base, end + 1):
            response = json.loads(stream.readline().decode())
            ack = response["ack"]

            print(f"ACK received: {ack}")

            if ack > next_expected:
                next_expected = ack

        # Slide the window or retransmit
        if next_expected == base:
            print(f"Retransmitting from Frame {base}")
        else:
            base = next_expected

        # Read window completion response
        response = json.loads(stream.readline().decode())

    print("\nAll frames transmitted and acknowledged.")

finally:
    try:
        stream.write(b'{"type":"quit"}\n')
        stream.flush()
        stream.close()
    except (OSError, BrokenPipeError):
        pass

    client.close()
    