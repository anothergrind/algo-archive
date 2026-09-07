"""Deliberately naive oracle for P3: per-cell outward scan, bubble-down gravity.

Only used by fuzz.py to differential-test code.py.
"""


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    R, C = map(int, rows[0].split())
    g = [list(rows[1 + i]) for i in range(R)]

    while True:
        mark = []
        for i in range(R):
            for j in range(C):
                if g[i][j] == ".":
                    continue
                l = r = j
                while l - 1 >= 0 and g[i][l - 1] == g[i][j]:
                    l -= 1
                while r + 1 < C and g[i][r + 1] == g[i][j]:
                    r += 1
                if r - l + 1 >= 3:
                    mark.append((i, j))
                    continue
                u = d = i
                while u - 1 >= 0 and g[u - 1][j] == g[i][j]:
                    u -= 1
                while d + 1 < R and g[d + 1][j] == g[i][j]:
                    d += 1
                if d - u + 1 >= 3:
                    mark.append((i, j))
        if not mark:
            break
        for i, j in mark:
            g[i][j] = "."
        moved = True                        # bubble every survivor down one at a time
        while moved:
            moved = False
            for i in range(R - 2, -1, -1):
                for j in range(C):
                    if g[i][j] != "." and g[i + 1][j] == ".":
                        g[i + 1][j], g[i][j] = g[i][j], "."
                        moved = True

    return ["".join(row) for row in g]
