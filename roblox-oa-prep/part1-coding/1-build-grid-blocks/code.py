"""P1 Build Grid Blocks -- reference solution. 2D prefix sums.

time  O(R*C)   -- one pass to build the prefix table, one to scan blocks
space O(R*C)   -- the prefix table
"""
import sys


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    R, C, k = map(int, rows[0].split())
    grid = [list(map(int, rows[1 + i].split())) for i in range(R)]

    # pre[i][j] = sum of grid[0..i-1][0..j-1]
    pre = [[0] * (C + 1) for _ in range(R + 1)]
    for i in range(R):
        prow, crow, grow = pre[i], pre[i + 1], grid[i]
        for j in range(C):
            crow[j + 1] = grow[j] + crow[j] + prow[j + 1] - prow[j]

    best = None
    for i in range(R - k + 1):
        top, bot = pre[i], pre[i + k]
        for j in range(C - k + 1):
            total = bot[j + k] - bot[j] - top[j + k] + top[j]
            if best is None or total > best[0]:
                best = (total, i, j)
    return ["%d %d %d" % best]


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
