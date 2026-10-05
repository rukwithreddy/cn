
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


data = input("Enter binary data: ")

if not data or any(bit not in "01" for bit in data):
    raise ValueError("Enter a valid binary string.")

# Append 16 zeros and calculate the CRC
remainder = get_remainder(data + "0" * 16)
codeword = data + remainder

print("\nOriginal data:", data)
print("CRC remainder:", remainder)
print("Generated codeword:", codeword)

# Create an erroneous codeword by flipping the last bit
corrupted = (
    codeword[:-1]
    + ("1" if codeword[-1] == "0" else "0")
)

print("Corrupted codeword:", corrupted)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

try:
    stream = client.makefile("rwb")

    for test_name, word in [
        ("Correct transmission", codeword),
        ("Corrupted transmission", corrupted)
    ]:
        message = {
            "test": test_name,
            "codeword": word
        }

        stream.write((json.dumps(message) + "\n").encode())
        stream.flush()

        response = json.loads(stream.readline().decode())

        print(f"\n{test_name}")
        print("Server remainder:", response["remainder"])
        print("Server result:", response["result"])

    stream.close()

finally:
    client.close()
    