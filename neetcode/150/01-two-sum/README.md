# 1. Two Sum

**Difficulty:** Easy

[View on LeetCode](https://leetcode.com/problems/two-sum/)

## Problem

Given an array of integers `nums` and an integer `target`, return the indices `i` and
`j` such that `nums[i] + nums[j] == target` and `i != j`.

You may assume that every input has exactly one pair of indices `i` and `j` that
satisfy the condition.

Return the answer with the smaller index first.

## Examples

**Example 1:**

```
Input: nums = [3,4,5,6], target = 7
Output: [0,1]
```

**Example 2:**

```
Input: nums = [4,5,6], target = 10
Output: [0,2]
```

**Example 3:**

```
Input: nums = [5,5], target = 10
Output: [0,1]
```

## Solution

See [`code.py`](code.py).

Brute force: check every pair with a nested loop and return the first pair that sums
to the target.

- **Time:** O(n^2)
- **Space:** O(1)
