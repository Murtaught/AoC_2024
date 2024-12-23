from __future__ import annotations

from dataclasses import dataclass
from typing import cast, Generator, Iterable

@dataclass
class Node:
    name: str
    nbrs: set[str]

neighbors: dict[str, set[str]] = {}

def add_neighbor(a: str, b: str) -> None:
    global neighbors
    if a not in neighbors:
        neighbors[a] = set()
    neighbors[a].add(b)

with open("input") as file:
    for line in file:
        a, b = line.strip().split('-')
        add_neighbor(a, b)
        add_neighbor(b, a)
        
# Solution (Part 1)
triples: set[str] = set()

def add_triple(names: list[str]) -> None:
    global triples
    triples.add('-'.join(sorted(names)))

for a, nbrs in neighbors.items():
    if not a.startswith('t'):
        continue

    for b in nbrs:
        for c in nbrs:
            if b != c and (c in neighbors[b]):
                assert (b in neighbors[c])
                add_triple([a, b, c])

print("ans (p1):", len(triples))

# Solution (Part 2)
largest_clique: list[str] = []

def bron_kerbosch_pivot(
        candidates: set[str], 
        excluded: set[str], 
        cur_clique: list[str], 
    ) -> None:

    global largest_clique

    if not candidates and not excluded:
        if len(cur_clique) > len(largest_clique):
            largest_clique = cur_clique.copy()
        return

    u = next(iter(candidates.union(excluded))) if candidates.union(excluded) else None
    if u:
        for v in candidates - neighbors[u]:
            bron_kerbosch_pivot(candidates & neighbors[v], excluded & neighbors[v], cur_clique + [v])
            excluded.add(v)
    else:
        for v in candidates:
            bron_kerbosch_pivot(candidates & neighbors[v], excluded & neighbors[v], cur_clique + [v])
            excluded.add(v)


bron_kerbosch_pivot(set(neighbors.keys()), set(), [])

ans_p2 = ','.join(sorted(largest_clique))
print("ans (p2):", ans_p2)
