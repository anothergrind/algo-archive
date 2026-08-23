# 49. Group Anagrams

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/group-anagrams/)

## Problem

Given an array of strings `strs`, group all anagrams together into sublists. You may
return the output in any order.

An anagram is a string that contains the exact same characters as another string, but
the order of the characters can be different.

## Examples

**Example 1:**

```
Input: strs = ["act","pots","tops","cat","stop","hat"]
Output: [["hat"],["act","cat"],["stop","pots","tops"]]
```

**Example 2:**

```
Input: strs = ["x"]
Output: [["x"]]
```

**Example 3:**

```
Input: strs = [""]
Output: [[""]]
```

## Solution

See [`code.py`](code.py).

Uses the sorted characters of each string as a dictionary key, so anagrams collide on
the same key and collect into the same list.

> **Note:** `code.py` uses `defaultdict` without importing it, so it raises a
> `NameError` as written — it needs `from collections import defaultdict`.

With that import added, the approach costs:

- **Time:** O(n * k log k), where k is the length of the longest string
- **Space:** O(n * k)
