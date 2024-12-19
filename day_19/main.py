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


with open("input") as file:
    lines = [line.strip() for line in file]
    PATTERNS = lines[0].split(', ')
    designs = lines[2:]

    
ans_p1 = 0
n = len(designs)
for i, design in enumerate(designs):
    # print(f"{i} / {n} ({i * 100.0 / n}%)")
    if can_construct(design):
        ans_p1 += 1

print("ans (p1):", ans_p1)

