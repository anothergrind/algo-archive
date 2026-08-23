# Fibonacci Number

## Problem

> The original prompt text is not stored in this repo. The statement below was
> reconstructed from the solution — paste the real prompt over it when convenient.

The Fibonacci numbers form a sequence in which each number is the sum of the two
preceding ones, starting from `0` and `1`:

```
F(0) = 0
F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1
```

Given `n`, return `F(n)`.

## Examples

Verified by running [`code.py`](code.py):

**Example 1:**

```
Input: n = 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1.
```

**Example 2:**

```
Input: n = 4
Output: 3
Explanation: F(4) = F(3) + F(2) = 2 + 1 = 3.
```

**Example 3:**

```
Input: n = 10
Output: 55
```

## Solution

See [`code.py`](code.py).

Straight recursion off the definition, with `0` and `1` as the base cases.

- **Time:** O(2^n)
- **Space:** O(n) for the call stack

> The recursion recomputes the same subproblems over and over, which is why the time
> cost is exponential. Memoizing the results, or iterating upward while keeping only
> the last two values, brings it to O(n).
