# Input
with open("input") as file:
    lines = [list(map(int, line.strip().split())) for line in file]

# Solution (Part 1)
def is_safe(line):
    steps = [b - a for (a, b) in zip(line, line[1:])]

    all_in_range = all(abs(step) in range(1, 4) for step in steps)
    all_positive = all(step >= 0 for step in steps)
    all_negative = all(step <= 0 for step in steps)

    return all_in_range and (all_positive or all_negative)

ans_p1 = sum(1 for p in map(is_safe, lines) if p)
print("ans (p1):", ans_p1)

# Solution (Part 2)
def is_safe_dampened(line):
    if is_safe(line):
        return True

    n = len(line)
    for i in range(n):
        line_copy = line[:]
        del line_copy[i]
        if is_safe(line_copy):
            return True

    return False

ans_p2 = sum(1 for p in map(is_safe_dampened, lines) if p)
print("ans (p2):", ans_p2)
