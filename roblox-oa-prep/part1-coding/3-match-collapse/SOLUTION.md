# P3 — Match and Collapse — solution

**Do not read this until you have an answer.** Back to the problem:
[README.md](README.md)

---

## Approach — mark into a set, clear, compact columns, repeat

The whole problem is keeping the three phases separate. Do them in one pass over the
grid and you will clear a run while you are still scanning it, which corrupts the runs
that cross it.

**Mark.** Sweep each row, grouping consecutive equal characters into maximal runs; if a
run is non-empty and at least 3 long, add all its coordinates to a set. Do the same
down each column. A `set` is the right container precisely because a cell at the
intersection of a horizontal and a vertical run gets added twice and must be cleared
once — using a list and clearing twice is harmless here, but the set also makes "was
anything marked?" a one-line check.

**Clear.** Only after both sweeps finish, write `.` into every marked cell. Marking and
clearing in the same loop is the classic wrong answer: an `L`-shaped match loses its
second arm because the shared cell was already blanked when the column sweep reached
it.

**Fall.** Per column, read out the survivors top-to-bottom into a list, then write them
back so they end at the bottom, padding the top with `.`. This is a stable compaction —
relative order is preserved, which is what "drop to the bottom" means. Doing it with
in-place swaps also works but is easy to get subtly wrong.

Loop until a round marks nothing. Each round clears at least three cells, so there are
at most `R*C/3` rounds; in practice cascades are a handful deep.

### Complexity

- **Time:** `O(R*C)` per round, `O((R*C)²/3)` worst case overall. At `R = C = 50` that
  is far inside any limit; the bound is loose because a round that clears only three
  cells cannot also be the round that sets up many more.
- **Space:** `O(R*C)` for the grid and the mark set.

### Reference solution

```python
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
```

Verified against `brute.py` — an oracle that marks by scanning outward from every cell
independently and applies gravity by repeated single-step bubbling — over 6000 random
boards on a two-and-three-symbol alphabet, which makes cascades and intersections
common. Run `python roblox-oa-prep/fuzz.py`.

---

## Hidden edge-case tests

### Hidden 1 — nothing ever matches (`tests/hidden1_no_match.in`)

```
3 4
aabb
bbaa
abab
```

```
aabb
bbaa
abab
```

Every run is exactly 2 long. The board is already stable, so the output is the input
verbatim and gravity never runs. Off-by-one in the run-length test (`>= 2` instead of
`>= 3`) wipes most of this board, and a solution that applies gravity unconditionally
before checking for marks would still pass here — but fails Hidden 3.

### Hidden 2 — the whole board clears (`tests/hidden2_full_clear.in`)

```
3 3
aaa
aaa
aaa
```

```
...
...
...
```

Every cell belongs to both a horizontal and a vertical run, so every cell is marked
twice. The result is an entirely empty board, which must still be printed as `R` lines
of `C` dots rather than as nothing.

### Hidden 3 — intersecting runs and a real fall (`tests/hidden3_intersection.in`)

```
4 5
b.a.b
aaaaa
..a..
..a..
```

```
.....
.....
.....
b...b
```

The `a` at row 1, column 2 sits in both a horizontal run of five and a vertical run of
four; both arms must clear in the same round. The two `b` blocks are untouched by the
match but are left floating in row 0, and must fall three rows to the bottom. A
solution that clears correctly but forgets gravity leaves them at the top; a solution
that clears sequentially loses one of the two arms and leaves stray `a` blocks behind.

---

## What this problem is testing

Faithful simulation under a rule that is easy to state and easy to implement wrongly.
The three failure modes it hunts are: marking and clearing interleaved, gravity that
does not preserve order, and stopping after one round instead of iterating to a fixed
point.
