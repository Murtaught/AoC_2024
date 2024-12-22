from __future__ import annotations

from collections import defaultdict, deque
from itertools import islice
from typing import cast, Generator

MASK = (1 << 24) - 1

def next_secret(secret: int, steps: int = 1) -> int:
    for _ in range(steps):
        secret = (secret ^ (secret <<  6)) & MASK
        secret = (secret ^ (secret >>  5)) & MASK
        secret = (secret ^ (secret << 11)) & MASK
    return secret

with open("input") as file:
    inputs = [int(line.strip()) for line in file]

# Solution (Part 1):
print("ans (p1):", sum(next_secret(input, 2000) for input in inputs))

# Solution (Part 2):
Seq = tuple[int, int, int, int]

def sequences(initial_secret: int) -> Generator[tuple[Seq, int]]:
    prev = initial_secret
    deq: deque[int] = deque()

    while True:
        cur = next_secret(prev)
        price = cur % 10

        deq.append(price - prev % 10)
        if len(deq) > 4:
            deq.popleft()
        if len(deq) == 4:
            yield (cast(Seq, tuple(deq)), price)

        prev = cur


bananas_by_seq: dict[Seq, int] = defaultdict(lambda: 0)
encountered: set[Seq]

for input in inputs:
    encountered = set()
    for seq, price in islice(sequences(input), 2000 - 4 + 1):
        if seq not in encountered:
            encountered.add(seq)
            bananas_by_seq[seq] += price

print("ans (p2):", max(bananas_by_seq.values()))
print("best sequence:", max(bananas_by_seq.keys(), key = lambda seq: bananas_by_seq.get(seq, 0)))
