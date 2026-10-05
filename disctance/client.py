
import socket
import json

n = int(input("Enter number of routers: "))

print("Enter the cost matrix (use 9999 for no direct link):")
cost = []

for i in range(n):
    row = list(map(int, input(f"Router {i}: ").split()))

    if len(row) != n:
        raise ValueError("Each row must contain n values.")

    cost.append(row)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12346))

client.sendall(json.dumps(cost).encode())

result = json.loads(client.recv(65536).decode())

print("\nShortest Costs from Each Router:")

for i, row in enumerate(result["distances"]):
    print(f"Router {i}: {row}")

client.close()
