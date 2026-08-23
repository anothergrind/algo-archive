# 1480. Running Sum of 1d Array

**Difficulty:** Easy

[View on LeetCode](https://leetcode.com/problems/running-sum-of-1d-array/)

## Problem

Given an array `nums`, we define a running sum of an array as
`runningSum[i] = sum(nums[0] … nums[i])`.

Return the running sum of `nums`.

## Examples

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: [1,3,6,10]
Explanation: Running sum is obtained as follows: [1, 1+2, 1+2+3, 1+2+3+4].
```

**Example 2:**

```
Input: nums = [1,1,1,1,1]
Output: [1,2,3,4,5]
Explanation: Running sum is obtained as follows: [1, 1+1, 1+1+1, 1+1+1+1, 1+1+1+1+1].
```

**Example 3:**

```
Input: nums = [3,1,2,10,1]
Output: [3,4,6,16,17]
```

## Constraints

- `1 <= nums.length <= 1000`
- `-10^6 <= nums[i] <= 10^6`

## Solution

See [`code.py`](code.py).

Walks the array from index 1 and adds each element to the one before it, so every slot
holds the running total by the time it is read. The accumulation happens in place, so
no second array is allocated.

- **Time:** O(n)
- **Space:** O(1) extra, since `nums` is modified in place and returned

> Note that this mutates the caller's list. LeetCode doesn't mind, but returning a new
> array would leave the input untouched.
