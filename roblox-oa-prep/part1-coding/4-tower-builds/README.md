# P4 — Tower Builds

**Difficulty:** Medium
**Suggested time:** 12 min (of the 60 min budget for all five)

---

## Description

You are stacking a tower out of blocks. `M` block types are available; type `i` has
height `h[i]`. You have an unlimited supply of every type.

The tower is built bottom to top, one block at a time, and must end at **exactly**
height `N`. For visual contrast, **two blocks of the same height may not be stacked
directly on top of each other.**

Two towers are different if they differ at any position, so order matters:
`1, 2, 1` and `2, 1, 2` are different towers.

Return the number of distinct towers, **modulo `10^9 + 7`**.

The empty tower has height 0 and is a valid tower.

---

## Input

```
N M
<M space-separated block heights>
```

## Output

A single integer: the tower count modulo `10^9 + 7`.

---

## Constraints

- `0 ≤ N ≤ 5000`
- `1 ≤ M ≤ 50`
- `1 ≤ h[i] ≤ 5000`, and the heights are **distinct**

The count grows exponentially in `N`, so it must be reduced modulo `10^9 + 7`
throughout — the exact value does not fit in any fixed-width integer.

---

## Example 1

Input:

```
4 2
1 2
```

Output:

```
1
```

Explanation: the only tower is `1, 2, 1`. Everything else fails the adjacency rule or
misses the height: `2, 2` stacks equal heights, `1, 1, 2` and `2, 1, 1` do too, and
`1, 1, 1, 1` is four in a row. There is no way to reach exactly 4 otherwise.

## Example 2

Input:

```
7 3
1 2 3
```

Output:

```
9
```

Explanation: the nine towers, listed bottom-to-top, are

```
1,2,1,2,1   1,2,1,3   1,2,3,1   1,3,1,2   1,3,2,1
2,1,3,1     2,3,2     3,1,2,1   3,1,3
```

Note `2,3,2` and `3,1,3` — a height may repeat in the tower, just not in adjacent
positions.

---

Reference solution, complexity notes and the hidden edge-case tests are in
[SOLUTION.md](SOLUTION.md) — don't open it until you have an answer.
