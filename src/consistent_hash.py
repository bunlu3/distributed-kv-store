import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes=None, virtual_nodes=3):
        self.ring = dict()
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)

    def add_node(self, node_id):
        for i in range(self.virtual_nodes):
            virtual_node_id = f"{node_id}#{i}"
            key = self._hash(virtual_node_id)
            self.ring[key] = node_id
            bisect.insort(self.sorted_keys, key)

    def remove_node(self, node_id):
        for i in range(self.virtual_nodes):
            virtual_node_id = f"{node_id}#{i}"
            key = self._hash(virtual_node_id)
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None
        key_hash = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, key_hash) % len(self.sorted_keys)
        ring_key = self.sorted_keys[idx]
        return self.ring[ring_key]

    def get_nodes_for_key(self, key, num_replicas=2):
        """Returns a list of num_replicas unique nodes for a given key"""
        if not self.ring:
            return []

        nodes = []
        key_hash = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, key_hash)

        while len(nodes) < num_replicas:
            i = idx % len(self.sorted_keys)
            node_id = self.ring[self.sorted_keys[i]]
            if node_id not in nodes:
                nodes.append(node_id)
            idx += 1

        return nodes
