#!/usr/bin/env python3
"""
MemoryGraph — append-only hash-chained episodic memory (no deletion of ethics trail).
"""
from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


def _stable_hash(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


@dataclass
class MemoryNode:
    node_id: str
    timestamp: float
    context: str
    payload: Dict[str, Any]
    prev_hash: str
    record_hash: str


class MemoryGraph:
    def __init__(self, path: str = "data/memory_graph.jsonl", max_nodes: int = 10000):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.nodes: List[MemoryNode] = []
        self.prev_hash = "GENESIS"
        self.max_nodes = max_nodes

    def store(self, context: str, payload: Dict[str, Any]) -> MemoryNode:
        ts = time.time()
        body = {
            "timestamp": ts,
            "context": context[:1000],
            "payload": payload,
            "prev_hash": self.prev_hash,
        }
        rh = _stable_hash(body)
        node = MemoryNode(
            node_id=rh[:16],
            timestamp=ts,
            context=body["context"],
            payload=payload,
            prev_hash=self.prev_hash,
            record_hash=rh,
        )
        self.nodes.append(node)
        self.prev_hash = rh
        if len(self.nodes) > self.max_nodes:
            self.nodes.pop(0)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(node), ensure_ascii=False) + "\n")
        return node

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for n in self.nodes:
            body = {
                "timestamp": n.timestamp,
                "context": n.context,
                "payload": n.payload,
                "prev_hash": prev,
            }
            if _stable_hash(body) != n.record_hash:
                return False
            prev = n.record_hash
        return True

    def size(self) -> int:
        return len(self.nodes)

    def recent(self, n: int = 10) -> List[Dict[str, Any]]:
        return [asdict(x) for x in self.nodes[-n:]]
