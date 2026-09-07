# P2 — Longest Play Session

**Difficulty:** Medium
**Suggested time:** 10 min (of the 60 min budget for all five)

---

## Description

A player's activity log is a list of `n` game IDs in the order they were played,
one entry per launch. The same game appearing twice in a row is two entries.

A **focused session** is any contiguous stretch of that log containing **at most `K`
distinct games**. Return the number of entries in the longest focused session.

---

## Input

```
n K
<n space-separated game IDs on one line>
```

When `n` is 0 the second line is present but empty.

## Output

A single integer: the length of the longest focused session.

---

## Constraints

- `0 ≤ n ≤ 2 * 10^5`
- `0 ≤ K ≤ n`
- Each game ID is 1–10 characters of `[a-z0-9]`. IDs are compared by exact match.

`n` up to `2 * 10^5` rules out checking every start position and extending from it —
that is `4 * 10^10` steps in the worst case. Aim for a single pass in which each entry
is examined a constant number of times.

---

## Example 1

Input:

```
10 2
ob ob jb jb jb ad ad jb bs bs
```

Output:

```
6
```

Explanation: entries 2 through 7 (0-indexed) are `jb jb jb ad ad jb` — six entries
drawing on only two distinct games, `jb` and `ad`. Extending left to index 1 adds
`ob` for a third game; extending right to index 8 adds `bs` for a third.

## Example 2

Input:

```
6 3
ob jb ad bs ob jb
```

Output:

```
3
```

Explanation: every game differs from its neighbours, so no stretch of four entries
can hold as few as three distinct games. Several stretches of three tie; the answer is
the length, so the tie does not matter.

---

Reference solution, complexity notes and the hidden edge-case tests are in
[SOLUTION.md](SOLUTION.md) — don't open it until you have an answer.
