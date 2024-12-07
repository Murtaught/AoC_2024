from enum import Enum

# Input
input = []
with open("input") as file:
    for line in file:
        target, xs = line.strip().split(':')
        target = int(target)
        xs = list(map(int, xs.strip().split()))
        input.append((target, xs))

# Solution
def pred_2(target, xs):
    n_op = len(xs) - 1
    assert n_op > 0

    n_mask = 1 << n_op

    for mask in range(n_mask):
        acc = xs[0]
        for i in range(1, len(xs)):
            if (mask & (1 << (i - 1))):
                acc *= xs[i]
            else:
                acc += xs[i]

        if acc == target:
            # print(f"Found solution: {target} = {strinfigy_solution(mask, xs)}")
            return True

    return False

class Op(Enum):
    ADD = 0
    MULT = 1
    CONCAT = 2

def compute(ops, xs):
    assert len(ops) + 1 == len(xs)
    acc = xs[0]
    for i in range(1, len(xs)):
        match ops[i - 1]:
            case Op.ADD:
                acc += xs[i]
            case Op.MULT:
                acc *= xs[i]
            case Op.CONCAT:
                acc = int(str(acc) + str(xs[i]))
    return acc

def strinfigy_solution(ops, xs):
    assert len(ops) + 1 == len(xs)
    ret = str(xs[0])
    for i in range(1, len(xs)):
        match ops[i - 1]:
            case Op.ADD:
                ret += ' + '
            case Op.MULT:
                ret += ' * '
            case Op.CONCAT:
                ret += ' || '
        ret += str(xs[i])
    return ret

def increment_ops(ops):
    n = len(ops)
    i = n - 1

    while i >= 0:
        next = ops[i].value + 1
        if next <= Op.CONCAT.value:
            ops[i] = Op(next)
            break
        else:
            ops[i] = Op.ADD
            i -= 1
    
    # Returns `True` if exhausted.
    return i < 0

def pred_3(target, xs):
    n_op = len(xs) - 1
    assert n_op > 0

    ops = [Op.ADD] * n_op
    exhausted = False

    while not exhausted:
        if compute(ops, xs) == target:
            return True
        exhausted = increment_ops(ops)

    return False

def solve(pred, progress=False):
    n = len(input)
    ans = 0
    for i, (target, xs) in enumerate(input):
        if progress:
            print(f"{i} / {n} ...")
        if pred(target, xs):
            ans += target
    return ans

print("ans (p1):", solve(pred_2))
print("ans (p2):", solve(pred_3))


