# 🔁 DistributedKV

**DistributedKV** is a fault-tolerant distributed key-value store written in Python.

It implements **consistent hashing**, **replication**, and **quorum-based reads/writes** to ensure high availability and resilience to node failures. Heartbeat monitoring enables failure detection and recovery simulation.

---

## 🚀 Features

-  **Consistent hashing ring** for scalable key distribution
-  **TCP-based node-to-node communication**
-  **Replication** with tunable **quorum (W+R > N)** logic
-  **Heartbeat-based failure detection**
-  **Simulated clients** and **dynamic recovery** of failed nodes

---

## 🧱 Project Structure

| File/Folder        | Purpose                                                      |
|--------------------|--------------------------------------------------------------|
| `src/node.py`      | Core node logic: TCP server, replication, heartbeat          |
| `src/utils.py`     | Common helper functions for hashing, quorum, etc.            |
| `client.py`        | CLI client for interacting with nodes                        |
| `client_route.py`  | Client-side logic to determine responsible node              |
| `run_cluster.py`   | Run a single cluster with N replicas                          |
| `run_multi_node.py`| Spin up multiple distributed nodes                           |

---

## 📸 Architecture

```mermaid
graph TD
    Client --> Router[Client Router]
    Router --> A[node-A]
    Router --> B[node-B]
    Router --> C[node-C]
    A <--> B
    B <--> C
    A <--> C
