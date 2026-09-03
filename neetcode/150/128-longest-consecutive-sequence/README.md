# 128. Longest Consecutive Sequence

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/)

## Problem

Given an unsorted array of integers `nums`, return the length of the longest sequence
of consecutive elements in the array.

A consecutive sequence is a sequence of elements in which each element is exactly one
greater than the previous element. The elements do not have to be adjacent in the
original array.

## Examples

**Example 1:**

```
Input: nums = [2,20,4,10,3,4,5]
Output: 4
Explanation: The longest consecutive sequence is [2,3,4,5].
```

**Example 2:**

```
Input: nums = [0,3,2,5,4,6,1,1]
Output: 7
Explanation: The longest consecutive sequence is [0,1,2,3,4,5,6].
```

## Solution

See [`code.py`](code.py).

`longestConsecutive` is the working solution. It puts every value in a set, then only
starts counting from a value whose predecessor is absent — that value is the start of
a run — and walks forward while the next value is present. Each run is walked once, so
the whole scan is linear.

- **Time:** O(n)
- **Space:** O(n)

`mySolution` in the same file is an earlier attempt kept for reference. It counts how
many values have a successor in the array rather than measuring run length, so it
returns the wrong answer whenever there is more than one run.
