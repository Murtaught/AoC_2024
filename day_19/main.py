import functools

@functools.cache
def can_construct(design: str) -> bool:
    if design == '':
        return True

    for pattern in PATTERNS:
        if design.startswith(pattern):
            if can_construct(design[len(pattern):]):
                return True

    return False

@functools.cache
def count_ways(design: str) -> int:
    if design == '':
        return 1

    total_ways = 0
    for pattern in PATTERNS:
        if design.startswith(pattern):
            total_ways += count_ways(design[len(pattern):])

    return total_ways

with open("input") as file:
    lines = [line.strip() for line in file]
    PATTERNS = lines[0].split(', ')
    designs = lines[2:]

    
ans_p1 = 0
ans_p2 = 0

n = len(designs)
for i, design in enumerate(designs):
    # print(f"{i} / {n} ({i * 100.0 / n}%)")
    ans_p1 += int(can_construct(design))
    ans_p2 += count_ways(design)

print("ans (p1):", ans_p1)
print("ans (p2):", ans_p2)

