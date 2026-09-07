# P1 — Best Build Block — solution

**Do not read this until you have an answer.** Back to the problem:
[README.md](README.md)

---

## Approach — 2D prefix sums

The naive solution re-adds every cell of every candidate block: `O(R·C·k²)`, which at
the stated bounds is around `10^12` operations. The fix is to make any block's sum a
constant-time lookup.

Build a table `pre` of size `(R+1) × (C+1)` where `pre[i][j]` is the sum of the
rectangle from `(0,0)` to `(i-1, j-1)`. Each entry is one addition and one subtraction
away from its neighbours:

```
pre[i+1][j+1] = grid[i][j] + pre[i+1][j] + pre[i][j+1] - pre[i][j]
```

The `- pre[i][j]` term is inclusion–exclusion: the region above and the region to the
left overlap in that corner, so it would otherwise be counted twice.

Then the sum of the `k × k` block anchored at `(i, j)` is four lookups:

```
pre[i+k][j+k] - pre[i+k][j] - pre[i][j+k] + pre[i][j]
```

Scan anchors in row-major order and keep the running best, replacing it only on a
**strictly** greater total. Because row-major order visits smaller rows first and,
within a row, smaller columns first, strict comparison gives exactly the required
tie-break for free — no explicit tie handling needed.

### Complexity

- **Time:** `O(R·C)` — one pass to build the table, one to scan anchors. Independent
  of `k`, which is the whole point.
- **Space:** `O(R·C)` for the prefix table. Can be reduced to `O(C)` by streaming one
  row band at a time if memory is tight, at the cost of clarity.

### Reference solution

```python
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
```

Verified against `brute.py` — a deliberately naive `O(R·C·k²)` re-summing oracle —
over 4000 random grids seeded toward ties, all-negative plots and all-equal plots.
Run it yourself with `python roblox-oa-prep/fuzz.py`.

---

## Hidden edge-case tests

### Hidden 1 — every cell negative (`tests/hidden1_all_negative.in`)

```
3 4 2
-9 -8 -7 -6
-5 -4 -3 -2
-1 -9 -9 -9
```

```
-18 0 2
```

The answer is the *least* negative block, not zero and not "no claim". Initialising
your best total to `0` instead of `None`/`-infinity` returns garbage here — this is
the single most common failure on this problem.

### Hidden 2 — every cell identical (`tests/hidden2_ties.in`)

```
4 4 2
2 2 2 2
2 2 2 2
2 2 2 2
2 2 2 2
```

```
8 0 0
```

All nine candidate blocks total 8. Only the tie-break decides, and it must land on
`0 0`. A `>=` comparison instead of `>` walks the answer to the last block, `2 2`.

### Hidden 3 — minimum grid at the value bound (`tests/hidden3_bounds.in`)

```
1 1 1
-1000000000
```

```
-1000000000 0 0
```

`R = C = k = 1`, so the loops run exactly once — an off-by-one in the `R - k + 1`
bound skips the only block and crashes or returns nothing. The value also confirms
you are not clamping negatives.

---

## What this problem is testing

Recognising that a per-query cost of `O(k²)` has to become `O(1)` before the
constraints are satisfiable — and that the standard inclusion–exclusion table is the
tool. The tie-break and the negative-initialisation trap are there to catch people who
get the algorithm right and the bookkeeping wrong.
