# 238. Product of Array Except Self

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/product-of-array-except-self/)

## Problem

Given an integer array `nums`, return an array `output` where `output[i]` is the
product of all the elements of `nums` except `nums[i]`.

Each product is guaranteed to fit in a 32-bit integer.

## Examples

**Example 1:**

```
Input: nums = [1,2,4,6]
Output: [48,24,12,8]
```

**Example 2:**

```
Input: nums = [-1,0,1,2,3]
Output: [0,-6,0,0,0]
```

## Constraints

- `2 <= nums.length <= 1000`
- `-20 <= nums[i] <= 20`

## Follow Up

Could you solve it in O(n) time without using the division operation?

## Solution

See [`code.py`](code.py).

Brute force: for each index, multiply every other element in a second pass.

- **Time:** O(n^2)
- **Space:** O(1) excluding the output array

> This does not yet meet the O(n) follow-up. The linear approach is a prefix-product
> pass followed by a suffix-product pass.
