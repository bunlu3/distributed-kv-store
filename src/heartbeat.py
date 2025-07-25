import json
import threading
import time
import socket

class HeartbeatMonitor:
    def __init__(self, self_id, peers, port_map, interval=2, timeout=6):
        self.self_id = self_id
        self.peers = peers  # list of node IDs to ping
        self.port_map = port_map  # node_id -> port
        self.interval = interval
        self.timeout = timeout
        self.last_seen = {peer: time.time() for peer in peers}
        self.failed = set()
        self.running = True

    def send_heartbeat(self, peer_id):
        try:
            port = self.port_map[peer_id]
            with socket.create_connection(("127.0.0.1", port), timeout=2) as sock:
                message = json.dumps({
                    "type": "HEARTBEAT",
                    "sender": self.self_id
                }).encode()

                sock.send(message)
                _ = sock.recv(1024)
                print(f"[DEBUG] Sent heartbeat to {peer_id}")
        except Exception as e:
            print(f"[ERROR] Failed to send heartbeat to {peer_id}: {e}")

    def heartbeat_loop(self):
        while self.running:
            now = time.time()
            for peer in self.peers:
                self.send_heartbeat(peer)

            for peer in self.peers:
                time_since_last = now - self.last_seen[peer]
                if time_since_last > self.timeout:
                    if peer not in self.failed:
                        print(f"💀 [WARN] Suspect node {peer} is down (last seen {int(time_since_last)}s ago)")
                        self.failed.add(peer)
                else:
                    if peer in self.failed:
                        print(f"✅ [INFO] Node {peer} is back")
                        self.failed.remove(peer)

            time.sleep(self.interval)

    def handle_heartbeat(self, sender_id):
        print(f"[DEBUG] Received heartbeat from {sender_id}")
        self.last_seen[sender_id] = time.time()

    def start(self):
        thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
        thread.start()
