from __future__ import annotations
from typing import Optional, Tuple

PROGRAM = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
N = len(PROGRAM)

def reverse(i: int, a_base: int) -> Optional[int]:
    if i < 0:
        return a_base // 8

    # The code below was manually converted from 3-bit code 
    # `PROGRAM` to Python with minor adjustments.

    # Let's try all `mod = a % 8`s!
    for mod in range(8):
        a = a_base + mod
        b1 = mod ^ 2
        c = a // (1 << b1)
        b2 = b1 ^ c ^ 3
        if (b2 % 8) == PROGRAM[i]:
            # Wow, it matches!
            if up := reverse(i - 1, a * 8):
                return up

    return None

print("ans (p2):", reverse(N - 1, 0))
