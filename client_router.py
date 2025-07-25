import socket
import json
from src.consistent_hash import ConsistentHashRing

NODE_PORTS = {
    "node-A": 5000,
    "node-B": 5001,
    "node-C": 5002,
}

ring = ConsistentHashRing(nodes=list(NODE_PORTS.keys()), virtual_nodes=5)

def send_command(node_id, command):
    port = NODE_PORTS[node_id]
    with socket.create_connection(("127.0.0.1", port)) as sock:
        sock.send(json.dumps(command).encode())
        response = sock.recv(1024)
        print(f"📤 Sent to {node_id}: {command}")
        print("📥 Response:", json.loads(response.decode()))

def route_command(command, W=2, R=1):
    key = command.get("key")
    node_ids = ring.get_nodes_for_key(key, num_replicas=3)  # N=3 total replicas

    if command["type"] == "PUT":
        success_count = 0
        for node_id in node_ids:
            try:
                send_command(node_id, command)
                success_count += 1
            except Exception as e:
                print(f"❌ Write to {node_id} failed: {e}")
        if success_count >= W:
            print(f"✅ PUT quorum met: {success_count}/{W}")
        else:
            print(f"❌ PUT quorum failed: only {success_count}/{W} writes succeeded")

    elif command["type"] == "GET":
        responses = []
        for node_id in node_ids:
            try:
                port = NODE_PORTS[node_id]
                with socket.create_connection(("127.0.0.1", port), timeout=2) as sock:
                    sock.send(json.dumps(command).encode())
                    response = sock.recv(1024)
                    parsed = json.loads(response.decode())
                    if parsed.get("status") == "OK":
                        responses.append(parsed["value"])
                        print(f"📤 Got value from {node_id}: {parsed['value']}")
                        if len(responses) >= R:
                            print(f"✅ GET quorum met: {len(responses)}/{R}")
                            print(f"🎯 Value: {responses[0]}")
                            return
            except Exception as e:
                print(f"❌ Read from {node_id} failed: {e}")
        print(f"❌ GET quorum failed: only {len(responses)}/{R} responses")


if __name__ == "__main__":
    route_command({"type": "PUT", "key": "apple", "value": "red"}, W=2)
    route_command({"type": "GET", "key": "apple"}, R=1)
