# P3 — Match and Collapse

**Difficulty:** Medium-Hard
**Suggested time:** 18 min (of the 60 min budget for all five)

---

## Description

A puzzle board is an `R × C` grid. Each cell holds a lowercase letter (a block) or
`.` (empty).

The board resolves in rounds. One round is:

1. **Mark.** Find every maximal run of **3 or more** identical blocks lying
   consecutively in a row, and every such run in a column. Mark every cell in every
   such run. Empty cells are never part of a run.
2. If nothing was marked, the board is stable — stop.
3. **Clear.** Empty every marked cell **simultaneously**. A cell that belongs to both
   a horizontal run and a vertical run is cleared once, and both runs clear in full.
4. **Fall.** In each column independently, the surviving blocks drop to the bottom,
   keeping their relative order. The vacated cells at the top of the column become `.`.

Repeat until a round marks nothing. Return the final board.

Clearing is simultaneous within a round, not sequential — resolve all marks against the
board as it stood at the start of the round, then clear them all at once.

---

## Input

```
R C
<R lines, each exactly C characters of [a-z.]>
```

## Output

`R` lines, each exactly `C` characters, giving the stable board.

---

## Constraints

- `1 ≤ R, C ≤ 50`
- Every grid line is exactly `C` characters long.
- Runs are strictly horizontal or vertical. Diagonals never match.

---

## Example 1

Input:

```
5 3
aaa
bcb
bcb
bcb
abc
```

Output:

```
...
...
...
...
abc
```

Explanation: in one round, row 0 is a horizontal run of three `a`, and each of the
three columns holds a vertical run of three across rows 1–3 (`b`, `c`, `b`). All twelve
cells are marked and cleared together. Only row 4 survives, and it is already at the
bottom, so nothing falls. The next round marks nothing.

## Example 2

Input:

```
4 3
abc
acb
xxx
abc
```

Output:

```
...
.bc
.cb
.bc
```

Explanation: this takes **two** rounds.

Round 1 marks only row 2, the horizontal run `xxx`. After clearing it, column 0 holds
`a, a, a` (rows 0, 1 and 3 falling into rows 1, 2, 3), column 1 holds `b, c, b` and
column 2 holds `c, b, c`. The board is now:

```
...
abc
acb
abc
```

Round 2 marks column 0's new vertical run of three `a` — a run that did not exist in
the input and only appeared because of the fall. Clearing it and letting the remaining
columns settle gives the answer. Round 3 marks nothing.

---

Reference solution, complexity notes and the hidden edge-case tests are in
[SOLUTION.md](SOLUTION.md) — don't open it until you have an answer.
