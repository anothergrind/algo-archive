"""Deliberately naive oracle for P1: re-sum every block from scratch.

time O(R*C*k^2). Only used by fuzz.py to differential-test code.py.
"""


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    R, C, k = map(int, rows[0].split())
    grid = [list(map(int, rows[1 + i].split())) for i in range(R)]

    best = None
    for i in range(R - k + 1):
        for j in range(C - k + 1):
            total = 0
            for di in range(k):
                for dj in range(k):
                    total += grid[i + di][j + dj]
            if best is None or total > best[0]:
                best = (total, i, j)
    return ["%d %d %d" % best]
