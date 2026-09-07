"""Deliberately naive oracle for P4: enumerate every sequence by DFS, no memo.

Exponential. Only used by fuzz.py on tiny N.
"""

MOD = 10 ** 9 + 7


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    N, M = map(int, rows[0].split())
    H = list(map(int, rows[1].split())) if len(rows) > 1 else []

    count = 0

    def walk(total, last):
        nonlocal count
        if total == N:
            count += 1
            return
        for t, h in enumerate(H):
            if t == last:
                continue
            if total + h <= N:
                walk(total + h, t)

    walk(0, -1)
    return [str(count % MOD)]
