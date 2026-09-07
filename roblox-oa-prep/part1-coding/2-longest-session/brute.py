"""Deliberately naive oracle for P2: try every start, extend with a set.

time O(n^2). Only used by fuzz.py to differential-test code.py.
"""


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    n, K = map(int, rows[0].split())
    plays = rows[1].split() if n and len(rows) > 1 else []

    best = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            seen.add(plays[j])
            if len(seen) > K:
                break
            if j - i + 1 > best:
                best = j - i + 1
    return [str(best)]
