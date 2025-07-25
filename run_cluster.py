from src.node import KeyValueNode
from rich.console import Console

console = Console()

if __name__ == "__main__":
    node = KeyValueNode(node_id="node-A", port=5000)
    console.print("✅ Server is running... waiting for clients.", style="bold cyan")
    node.start()
