from __future__ import annotations

from dataclasses import dataclass
from typing import cast, Generator, Iterable

@dataclass
class Node:
    name: str
    nbrs: set[str]

nodes: dict[str, Node] = {}

def get_or_create_node(name: str) -> Node:
    global nodes
    if name not in nodes:
        nodes[name] = Node(name, set())
    return nodes[name]

with open("input") as file:
    for line in file:
        a, b = line.strip().split('-')
        get_or_create_node(a).nbrs.add(b)
        get_or_create_node(b).nbrs.add(a)
        
# Solution (Part 1)
triples: set[str] = set()

def add_triple(names: list[str]) -> None:
    global triples
    triples.add('-'.join(sorted(names)))

for node in nodes.values():
    a = node.name
    if not a.startswith('t'):
        continue

    for b in node.nbrs:
        for c in node.nbrs:
            if b != c and (c in nodes[b].nbrs):
                assert (b in nodes[c].nbrs)
                add_triple([a, b, c])

print("ans (p1):", len(triples))
