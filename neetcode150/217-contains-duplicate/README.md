# 217. Contains Duplicate

**Difficulty:** Easy

[View on LeetCode](https://leetcode.com/problems/contains-duplicate/)

## Problem

Given an integer array `nums`, return `true` if any value appears more than once in
the array, otherwise return `false`.

## Examples

**Example 1:**

```
Input: nums = [1,2,3,3]
Output: true
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: false
```

## Solution

See [`code.py`](code.py).

Brute force: compare every element against every later element with a nested loop.

- **Time:** O(n^2)
- **Space:** O(1)
