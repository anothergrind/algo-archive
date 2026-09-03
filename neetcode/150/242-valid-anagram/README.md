# 242. Valid Anagram

**Difficulty:** Easy

[View on LeetCode](https://leetcode.com/problems/valid-anagram/)

## Problem

Given two strings `s` and `t`, return `true` if the two strings are anagrams of each
other, otherwise return `false`.

An anagram is a string that contains the exact same characters as another string, but
the order of the characters can be different.

## Examples

**Example 1:**

```
Input: s = "racecar", t = "carrace"
Output: true
```

**Example 2:**

```
Input: s = "jar", t = "jam"
Output: false
```

## Constraints

- `s` and `t` consist of lowercase English letters.

## Solution

See [`code.py`](code.py).

Builds a character-count dictionary for each string and compares them.

> **Note:** this solution is currently incorrect. The `if s_dict == t_dict` check sits
> *inside* the loop over `t`, so it can return `True` as soon as a prefix of `t`
> matches, before the rest of the string is counted. The comparison belongs after the
> loop.
