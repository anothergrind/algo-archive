# 347. Top K Frequent Elements

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/top-k-frequent-elements/)

## Problem

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements
within the array.

The test cases are generated such that the answer is always unique. You may return the
output in any order.

## Examples

**Example 1:**

```
Input: nums = [1,2,2,3,3,3], k = 2
Output: [2,3]
```

**Example 2:**

```
Input: nums = [7,7], k = 1
Output: [7]
```

## Constraints

- `1 <= nums.length <= 10^4`
- `-1000 <= nums[i] <= 1000`
- `1 <= k <=` number of distinct elements in `nums`

## Solution

See [`code.py`](code.py).

Counts occurrences into a dictionary, then repeats `k` times: take the key with the
highest count, append it to the result, and pop it so the next `max` finds the next
most frequent value.

- **Time:** O(n + k * d), where d is the number of distinct values
- **Space:** O(d)

> **Note:** this mutates the frequency dictionary as it goes. That is what makes the
> repeated `max` work, but it means the counts are gone afterwards.
