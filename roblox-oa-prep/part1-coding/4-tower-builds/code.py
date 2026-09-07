"""P4 Tower Builds -- reference solution. DP over height, keyed on last block.

ways[s][t] = sequences summing to s whose last block is type t.
Using tot[s] = sum_t ways[s][t], the "not the same as last" transition is
tot[s] - ways[s][t], which drops the inner loop over previous types.

time  O(N*M)
space O(N*M)
"""
import sys

MOD = 10 ** 9 + 7


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    N, M = map(int, rows[0].split())
    H = list(map(int, rows[1].split())) if len(rows) > 1 else []

    if N == 0:
        return ["1"]

    ways = [[0] * M for _ in range(N + 1)]
    for t, h in enumerate(H):
        if h <= N:
            ways[h][t] = (ways[h][t] + 1) % MOD

    for s in range(1, N + 1):
        # every contribution to ways[s] is final: heights are >= 1, so all
        # transitions move strictly forward
        tot = sum(ways[s]) % MOD
        row = ways[s]
        for t, h in enumerate(H):
            ns = s + h
            if ns <= N:
                ways[ns][t] = (ways[ns][t] + tot - row[t]) % MOD

    return [str(sum(ways[N]) % MOD)]


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
