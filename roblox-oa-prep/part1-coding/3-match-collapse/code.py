"""P3 Match and Collapse -- reference solution. Sweep for runs, clear, gravity.

time  O(R*C*(R+C)) worst case -- each round is O(R*C) and there are O(R*C/3) rounds
                                 at most, but in practice rounds are few
space O(R*C)
"""
import sys


def find_marks(g, R, C):
    mark = set()
    for i in range(R):                      # horizontal runs
        j = 0
        while j < C:
            k = j
            while k < C and g[i][k] == g[i][j]:
                k += 1
            if g[i][j] != "." and k - j >= 3:
                mark.update((i, t) for t in range(j, k))
            j = k
    for j in range(C):                      # vertical runs
        i = 0
        while i < R:
            k = i
            while k < R and g[k][j] == g[i][j]:
                k += 1
            if g[i][j] != "." and k - i >= 3:
                mark.update((t, j) for t in range(i, k))
            i = k
    return mark


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    R, C = map(int, rows[0].split())
    g = [list(rows[1 + i]) for i in range(R)]

    while True:
        mark = find_marks(g, R, C)
        if not mark:
            break
        for i, j in mark:                   # clear simultaneously
            g[i][j] = "."
        for j in range(C):                  # gravity: survivors fall, order kept
            col = [g[i][j] for i in range(R) if g[i][j] != "."]
            pad = R - len(col)
            for i in range(R):
                g[i][j] = "." if i < pad else col[i - pad]

    return ["".join(row) for row in g]


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
