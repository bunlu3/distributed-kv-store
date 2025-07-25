from consistent_hash import ConsistentHashRing

ring = ConsistentHashRing(nodes=["node-A", "node-B", "node-C"], virtual_nodes=5)

print("\nResponsible nodes for key = 'apple':")
print(ring.get_nodes_for_key("apple", num_replicas=2))

print("\nResponsible nodes for key = 'banana':")
print(ring.get_nodes_for_key("banana", num_replicas=2))
