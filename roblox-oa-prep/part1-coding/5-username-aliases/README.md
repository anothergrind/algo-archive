# P5 — Username Aliases

**Difficulty:** Easy-Medium
**Suggested time:** 8 min (of the 60 min budget for all five)

---

## Description

Moderation wants to spot accounts that are cosmetic variations of one another.

Reduce each username to its **canonical form**:

1. Lowercase every character.
2. Delete every `_`, `.` and `-`.
3. Delete the trailing run of digits, if any — **unless** doing so would leave nothing,
   in which case keep the digits.

Two usernames are **aliases** when their canonical forms are identical. Group the
usernames by canonical form and report every group.

Exact duplicate usernames — identical character for character, before any
normalisation — are the same account listed twice. Keep only the first occurrence.

---

## Input

```
n
<n lines, one username each>
```

## Output

One line per group:

```
<canonical_form> <size> <member1> <member2> ...
```

Members are listed in **order of first appearance in the input**, in their original
spelling.

Groups are ordered by **size descending**; groups of equal size are ordered by
**canonical form ascending (ASCII)**.

When `n` is 0, print nothing.

---

## Constraints

- `0 ≤ n ≤ 10^5`
- Each username is 1–20 characters drawn from `[A-Za-z0-9_.-]`
- Every username contains at least one alphanumeric character

Note that step 3 removes only a **trailing** run of digits. Digits elsewhere survive:
`a1b` canonicalises to `a1b`, not `ab`.

---

## Example 1

Input:

```
6
Builder_Bob
builderbob
BUILDER.BOB
noob123
noob
xXx_Sniper_xXx
```

Output:

```
builderbob 3 Builder_Bob builderbob BUILDER.BOB
noob 2 noob123 noob
xxxsniperxxx 1 xXx_Sniper_xXx
```

Explanation: the first three all reduce to `builderbob` — one via the underscore rule,
one already canonical, one via lowercasing and the dot rule. `noob123` loses its
trailing digits and joins `noob`. The last name has no aliases but is still reported as
a group of one.

## Example 2

Input:

```
4
alpha
ALPHA
beta1
BETA
```

Output:

```
alpha 2 alpha ALPHA
beta 2 beta1 BETA
```

Explanation: both groups have size 2, so the tie is broken on canonical form, and
`alpha` sorts before `beta`.

---

Reference solution, complexity notes and the hidden edge-case tests are in
[SOLUTION.md](SOLUTION.md) — don't open it until you have an answer.
