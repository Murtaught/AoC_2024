import re

# Input
with open("input") as file:
    input = file.read().strip()

# Solution (Part 1)
mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

ans_p1 = 0
for m in mul_re.finditer(input):
    a = int(m.group(1))
    b = int(m.group(2))
    ans_p1 += a * b

print("ans (p1):", ans_p1)

# Solution (Part 2)
mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

ans_p2 = 0
enabled = True
for m in mul_re.finditer(input):
    instr = m.group(0)
    if instr == "do()":
        enabled = True
    elif instr == "don't()":
        enabled = False
    else:
        assert instr.startswith("mul")
        if enabled:
            a = int(m.group(1))
            b = int(m.group(2))
            ans_p2 += a * b

print("ans (p2):", ans_p2)
