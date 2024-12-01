# Input
with open("input0") as file:
    lines = [list(map(int, line.strip().split())) for line in file]
    lines = list(map(list, zip(*lines)))

xs, ys = lines

# Common preparation
xs.sort()
ys.sort()

assert len(xs) == len(ys)
n = len(xs)

# Solution (Part 1)
ans_p1 = 0
for i in range(n):
    ans_p1 += abs(xs[i] - ys[i])

print("ans (p1):", ans_p1)

# Solution (Part 2)
ans_p2 = 0
for x in xs:
    ans_p2 += x * ys.count(x)

print("ans (p2):", ans_p2)
