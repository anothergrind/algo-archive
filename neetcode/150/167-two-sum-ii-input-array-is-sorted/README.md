# 167. Two Sum II - Input Array Is Sorted

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

## Problem

Given an array of integers `numbers` that is sorted in non-decreasing order, return the
indices (**1-indexed**) of two numbers, `[index1, index2]`, such that they add up to a
given target number `target` and `index1 < index2`.

Note that `index1` and `index2` cannot be equal, so you may not use the same element
twice.

There will always be exactly one valid solution.

Your solution must use O(1) additional space.

## Examples

**Example 1:**

```
Input: numbers = [1,2,3,4], target = 3
Output: [1,2]
Explanation: The sum of 1 and 2 is 3. Since we are assuming a 1-indexed array,
index1 = 1, index2 = 2. We return [1,2].
```

## Solution

See [`code.py`](code.py).

Brute force over pairs, converting the 0-based loop indices to 1-based on return.

> **Note:** this solution is currently incorrect. The inner loop runs
> `for j in range(1, len(numbers))` independently of `i`, so `j` can equal or trail
> `i` — meaning the same element can be paired with itself and the `index1 < index2`
> requirement is not enforced. The inner loop should start at `i + 1`.
>
> It also does not meet the O(1)-space, O(n)-time bar the problem is really asking
> for; the intended approach is two pointers from both ends of the sorted array.
