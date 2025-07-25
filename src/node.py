import socket
import threading
import json
from rich import print
from src.heartbeat import HeartbeatMonitor

class KeyValueNode:
    def __init__(self, node_id, host='127.0.0.1', port=5000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.store = {}

        # --- Heartbeat Setup ---
        ALL_NODES = {
            "node-A": 5000,
            "node-B": 5001,
            "node-C": 5002,
        }
        peers = [n for n in ALL_NODES if n != self.node_id]
        self.heartbeat = HeartbeatMonitor(self.node_id, peers, ALL_NODES)

        # --- TCP Server Setup ---
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        # --- Start heartbeat monitor ---
        self.heartbeat.start()

        print(f"[bold green]Node {self.node_id} started at {self.host}:{self.port}[/bold green]")

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    try:
                        request = json.loads(data.decode())
                        response = self.process_command(request)
                        client_socket.send(json.dumps(response).encode())
                    except json.JSONDecodeError:
                        print("[red]Received non-JSON or partial data, ignoring.[/red]")
                    except Exception as e:
                        print(f"[red]Command handling error:[/red] {e}")
                except Exception as e:
                    print(f"[red]Connection error:[/red] {e}")
                    break

    def process_command(self, req):
        cmd = req.get("type")
        key = req.get("key")
        value = req.get("value")

        if cmd == "HEARTBEAT":
            sender = req.get("sender")
            if sender:
                self.heartbeat.handle_heartbeat(sender)
            return {"status": "OK"}
        elif cmd == "PUT":
            self.store[key] = value
            return {"status": "OK", "message": f"Stored key '{key}'"}
        elif cmd == "GET":
            if key in self.store:
                return {"status": "OK", "value": self.store[key]}
            else:
                return {"status": "ERROR", "message": "Key not found"}
        elif cmd == "DELETE":
            if key in self.store:
                del self.store[key]
                return {"status": "OK", "message": f"Deleted key '{key}'"}
            else:
                return {"status": "ERROR", "message": "Key not found"}
        else:
            return {"status": "ERROR", "message": "Unknown command"}

    def start(self):
        while True:
            client, addr = self.server.accept()
            print(f"[yellow]Connection from {addr}[/yellow]")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
