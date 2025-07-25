from multiprocessing import Process
from src.node import KeyValueNode

def start_node(node_id, port):
    node = KeyValueNode(node_id=node_id, port=port)
    node.start()

if __name__ == "__main__":
    nodes = [("node-A", 5000), ("node-B", 5001), ("node-C", 5002)]

    for node_id, port in nodes:
        p = Process(target=start_node, args=(node_id, port))
        p.start()
