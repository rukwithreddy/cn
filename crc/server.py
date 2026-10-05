
import socket
import json

HOST = "127.0.0.1"
PORT = 12348

GENERATOR = "10001000000100001"


def get_remainder(bits):
    data = list(bits)

    for i in range(len(data) - 16):
        if data[i] == "1":
            for j in range(17):
                data[i + j] = str(
                    int(data[i + j]) ^ int(GENERATOR[j])
                )

    return "".join(data[-16:])


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("CRC Server waiting for client...")

try:
    conn, addr = server.accept()
    print("Connected to:", addr)

    with conn:
        stream = conn.makefile("rwb")

        for _ in range(2):
            line = stream.readline()

            if not line:
                break

            msg = json.loads(line.decode())
            codeword = msg["codeword"]
            test_name = msg["test"]

            remainder = get_remainder(codeword)

            print(f"\nTest: {test_name}")
            print("Received codeword:", codeword)
            print("CRC remainder:", remainder)

            if remainder == "0000000000000000":
                result = "NO ERROR DETECTED"
            else:
                result = "ERROR DETECTED"

            print("Result:", result)

            response = {
                "remainder": remainder,
                "result": result
            }

            stream.write((json.dumps(response) + "\n").encode())
            stream.flush()

finally:
    server.close()
    print("\nServer closed.")
