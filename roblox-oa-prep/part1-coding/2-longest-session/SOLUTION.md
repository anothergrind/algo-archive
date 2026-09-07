# P2 — Longest Play Session — solution

**Do not read this until you have an answer.** Back to the problem:
[README.md](README.md)

---

## Approach — variable-size sliding window

Keep a window `[left, right]` and a count of how many times each game appears inside
it. The number of distinct games is just the size of that map.

Advance `right` one entry at a time. After adding an entry, if the window now holds
more than `K` distinct games, advance `left` — decrementing counts and deleting keys
that hit zero — until it is legal again. Record the best width seen.

The window never shrinks below legal and never needs to restart, because a window that
is legal stays legal when you drop entries from the left. Each index is added once and
removed at most once, so the two pointers together do `O(n)` work even though the inner
`while` looks nested.

The deletion is the part people get wrong: you must `del` the key when its count
reaches zero, not merely leave a zero behind. `len(counts)` is the distinct count, and
a lingering zero-valued key inflates it forever.

### Complexity

- **Time:** `O(n)` — each index enters and leaves the window at most once.
- **Space:** `O(K)` — the window never holds more than `K + 1` distinct keys.

### Reference solution

```python
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
```

Verified against `brute.py` — a naive `O(n²)` try-every-start oracle — over 4000
random logs with `K` spanning `0` to `n + 1`. Run `python roblox-oa-prep/fuzz.py`.

---

## Hidden edge-case tests

### Hidden 1 — `K = 0` (`tests/hidden1_k_zero.in`)

```
5 0
ob jb ad bs ob
```

```
0
```

Zero distinct games are allowed, so the only legal window is the empty one. The
`while len(counts) > K` loop drives `left` past `right`, giving a width of zero — which
is correct and must not be reported as 1. Code that assumes the answer is at least 1,
or that initialises `best = 1`, fails here.

### Hidden 2 — every entry identical (`tests/hidden2_all_same.in`)

```
7 1
zz zz zz zz zz zz zz
```

```
7
```

The whole log is one focused session. The window never shrinks, so `left` stays at 0 —
this catches implementations that advance `left` unconditionally rather than only while
the window is illegal.

### Hidden 3 — `K` larger than the number of games (`tests/hidden3_k_exceeds.in`)

```
1 9
solo
```

```
1
```

`K` exceeds both `n` and the distinct count. Nothing is ever evicted and the answer is
the whole log. Also the minimum non-empty input, which catches off-by-one loop bounds.

---

## What this problem is testing

Whether you reach for the two-pointer window instead of the nested scan once the
constraint makes `O(n²)` impossible — and whether your window bookkeeping is exact.
`K = 0` and the zero-count key deletion are the two places a working-looking solution
quietly returns the wrong number.
