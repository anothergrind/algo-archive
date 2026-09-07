# P4 — Tower Builds — solution

**Do not read this until you have an answer.** Back to the problem:
[README.md](README.md)

---

## Approach — DP keyed on height *and* last block

The adjacency rule means the running height is not a sufficient state: whether you may
place block `t` next depends on what is directly beneath. So carry the last block in
the state.

Let `ways[s][t]` be the number of towers of height exactly `s` whose topmost block is
type `t`. Seed it with the single-block towers: `ways[h[t]][t] += 1` for every type
whose height fits. Then for each height `s` in increasing order, extend every tower
ending there by any type other than its own:

```
ways[s + h[t]][t] += sum over u != t of ways[s][u]
```

That inner sum is the whole cost — `O(M)` per transition, `O(N·M²)` overall, which at
`N = 5000, M = 50` is 12.5 million inner steps and is uncomfortably slow in Python.

**The optimisation:** let `tot[s]` be the sum of `ways[s][*]`. Then

```
sum over u != t of ways[s][u]  ==  tot[s] - ways[s][t]
```

so each transition is `O(1)` and the whole DP is `O(N·M)` — 250 000 steps.

Processing `s` in increasing order is what makes this sound: every height is at least
1, so all transitions move strictly forward and `ways[s]` is final by the time `s` is
read. If heights of 0 were allowed the recurrence would be circular.

`N = 0` is answered directly: the empty tower is the one and only tower, so the answer
is 1, not 0. This is the case a straight loop over `1..N` silently returns 0 for.

### Complexity

- **Time:** `O(N·M)`.
- **Space:** `O(N·M)`, reducible to `O(max(h)·M)` with a rolling window.

### Reference solution

```python
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
```

`(tot - row[t]) % MOD` can go negative before the `%`; Python's modulo returns a
non-negative result, so this is safe here. In C++ or Java you must add `MOD` first.

Verified against `brute.py` — a plain exhaustive DFS with no memoisation — over 4000
random inputs with `N ≤ 12`, and cross-checked directly on the two samples.
Run `python roblox-oa-prep/fuzz.py`.

---

## Hidden edge-case tests

### Hidden 1 — zero height (`tests/hidden1_zero_height.in`)

```
0 2
3 5
```

```
1
```

The empty tower counts. Neither block fits, but that is irrelevant. Any solution whose
main loop starts at 1 and returns `sum(ways[0])` gives 0 here.

### Hidden 2 — one block type that cannot repeat (`tests/hidden2_single_type.in`)

```
4 1
2
```

```
0
```

Reaching 4 needs `2, 2`, which the adjacency rule forbids, and there is no alternative
type to break them up. The answer is a legitimate 0 — not an error, and not 1. This is
the case that catches a `tot[s]` transition that forgot to subtract `ways[s][t]`:
without the subtraction it happily returns 1.

### Hidden 3 — maximum height, real modular reduction (`tests/hidden3_max_mod.in`)

```
5000 3
1 2 3
```

```
337954009
```

The true count has thousands of digits. In Python an unreduced accumulator produces
the right answer eventually but takes far too long on bignum arithmetic; in a
fixed-width language it overflows to garbage. Either way the modulus has to be applied
inside the loop, not at the end.

---

## What this problem is testing

Spotting that "no two adjacent the same" forces the last-choice into the DP state, and
then noticing that the `O(M)` inner sum collapses to a total-minus-self subtraction.
`N = 0` and the single-type case are there to catch base-case and transition bugs that
larger inputs hide.
