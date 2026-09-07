# P1 — Best Build Block

**Difficulty:** Medium
**Suggested time:** 12 min (of the 60 min budget for all five)

---

## Description

A Roblox build plot is an `R × C` grid. Each cell holds an integer **value score** —
positive where a player has placed something worth keeping, negative where the terrain
would cost more to clear than it is worth.

You are placing a single square **claim** of size `k × k`. The claim must lie entirely
inside the plot and must be axis-aligned — no rotation, no partial cells.

Return the largest total value score any `k × k` claim can cover, together with the
position of that claim.

If several claims tie for the largest total, return the one whose top-left corner has
the **smallest row index**; if still tied, the **smallest column index**.

---

## Input

```
R C k
<R lines, each C space-separated integers>
```

## Output

A single line:

```
<max_total> <row> <col>
```

where `row` and `col` are the **0-indexed** coordinates of the winning claim's
top-left cell.

---

## Constraints

- `1 ≤ k ≤ min(R, C)`
- `1 ≤ R, C` and `R * C ≤ 10^6`
- `-10^9 ≤ grid[i][j] ≤ 10^9`

The value-score bound and the plot bound together mean a total can reach `10^15`, so
it does not fit in a 32-bit integer.

`R * C ≤ 10^6` with `k` as large as `1000` rules out re-summing each block: that is
up to `10^6` positions × `10^6` cells. Aim for a solution that touches each cell a
constant number of times regardless of `k`.

---

## Example 1

Input:

```
4 5 2
1 2 -1 4 0
3 -2 5 1 1
0 6 -3 2 4
7 1 0 -5 2
```

Output:

```
14 2 0
```

Explanation: the `2 × 2` claim with its top-left corner at row 2, column 0 covers
`0, 6, 7, 1`, totalling 14. No other `2 × 2` claim reaches it — the next best is
`-1, 4, 5, 1` at row 0, column 2, totalling 9.

## Example 2

Input:

```
3 3 3
1 1 1
1 1 1
1 1 1
```

Output:

```
9 0 0
```

Explanation: `k` equals both dimensions, so exactly one claim is possible.

---

Reference solution, complexity notes and the hidden edge-case tests are in
[SOLUTION.md](SOLUTION.md) — don't open it until you have an answer.
