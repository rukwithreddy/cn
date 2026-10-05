
import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12346))
server.listen(1)

print("Server waiting for client...")

conn, addr = server.accept()
print("Connected to:", addr)

data = conn.recv(65536).decode()
cost = json.loads(data)

n = len(cost)
dist = [row[:] for row in cost]
nexthop = [[j if cost[i][j] < 9999 else -1
            for j in range(n)] for i in range(n)]

# Distance Vector Routing
for _ in range(n):
    changed = False
    old = [row[:] for row in dist]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if cost[i][k] < 9999 and old[k][j] < 9999:
                    new_cost = cost[i][k] + old[k][j]

                    if new_cost < dist[i][j]:
                        dist[i][j] = new_cost
                        nexthop[i][j] = k
                        changed = True

    if not changed:
        break

print("\nFinal Routing Tables")

for i in range(n):
    print(f"\nRouter {i}")
    print("Destination\tCost\tNext Hop")

    for j in range(n):
        hop = nexthop[i][j]
        hop_text = "-" if i == j else (
            str(hop) if hop != -1 else "Unreachable"
        )
        cost_text = (
            "INF" if dist[i][j] >= 9999 else str(dist[i][j])
        )
        print(f"{j}\t\t{cost_text}\t{hop_text}")

conn.sendall(json.dumps({
    "distances": dist,
    "next_hops": nexthop
}).encode())

conn.close()
server.close()
