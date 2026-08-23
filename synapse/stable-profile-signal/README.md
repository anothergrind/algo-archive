# Stable Profile Signal

## Problem

> The original prompt text is not stored in this repo. The statement below was
> reconstructed from the solution and the author's notes — paste the real prompt over
> it when convenient.

A profile signal is transformed by replacing it with the sum of the squares of its
digits, repeatedly.

A signal is **stable** if repeating that transformation eventually reaches `1`. If it
instead falls into a cycle that never reaches `1`, it is not stable.

Given an integer `profile_signal`, return `true` if it is stable and `false` otherwise.

## Examples

Verified by running [`code.py`](code.py):

**Example 1:**

```
Input: profile_signal = 19
Output: true
Explanation: 1^2 + 9^2 = 82, 8^2 + 2^2 = 68, 6^2 + 8^2 = 100, 1^2 + 0^2 + 0^2 = 1.
```

**Example 2:**

```
Input: profile_signal = 2
Output: false
Explanation: the sequence enters a cycle that never reaches 1.
```

## Solution

See [`code.py`](code.py).

Keeps a set of every value already seen. On each pass, return `true` if the value is
`1`, return `false` if the value has been seen before (a cycle), otherwise record it
and compute the next value by summing the squares of its digits.

The set is what makes the loop terminate — without it, a non-stable signal would spin
forever.

- **Time:** O(log n) per transformation, over a bounded number of steps
- **Space:** O(1) bounded, since values quickly fall into a small range

> This is a themed version of what is otherwise the classic "happy number" problem.
