# DistributedKV

DistributedKV is a distributed key-value store written in Python.  
It implements consistent hashing, replication, and quorum-based reads/writes to ensure fault tolerance and high availability.

## Features
- Consistent hashing ring
- TCP-based node-to-node communication
- Replication (N), with quorum (W+R > N)
- Heartbeat-based failure detection
- Simulated concurrent clients and node recovery

## Structure
- `src/node.py`: core node logic (TCP server, local store, replication handler)
- `run_cluster.py`: spin up multiple nodes
- `src/utils.py`: common helper functions