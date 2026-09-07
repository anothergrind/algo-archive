"""P2 Longest Play Session -- reference solution. Variable-size sliding window.

time  O(n)  -- each index enters and leaves the window at most once
space O(K)  -- at most K+1 distinct ids are ever counted
"""
import sys


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    n, K = map(int, rows[0].split())
    plays = rows[1].split() if n and len(rows) > 1 else []

    counts = {}
    best = left = 0
    for right in range(n):
        g = plays[right]
        counts[g] = counts.get(g, 0) + 1
        while len(counts) > K:
            out = plays[left]
            counts[out] -= 1
            if counts[out] == 0:
                del counts[out]
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return [str(best)]


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
