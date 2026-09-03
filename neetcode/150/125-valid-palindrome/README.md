# 125. Valid Palindrome

**Difficulty:** Easy

[View on LeetCode](https://leetcode.com/problems/valid-palindrome/)

## Problem

Given a string `s`, return `true` if it is a palindrome, otherwise return `false`.

A palindrome reads the same forwards and backwards once non-alphanumeric characters
are removed and casing is ignored.

## Examples

**Example 1:**

```
Input: s = "Was it a car or a cat I saw?"
Output: true
Explanation: After removing non-alphanumeric characters and lowercasing,
"wasitacaroracatisaw" reads the same forwards and backwards.
```

**Example 2:**

```
Input: s = "tab a cat"
Output: false
Explanation: "tabacat" is not a palindrome.
```

## Solution

See [`code.py`](code.py).

Lowercases the string and compares it against its reverse, skipping characters that
are not alphanumeric.

> **Note:** this solution does not run. `s_comp.alnum()` is not a string method — the
> real one is `str.isalnum()`, and it needs to be called on a single character
> (`s_comp[i].isalnum()`) rather than the whole string. The skipping logic also needs
> rework: dropping a character from one side without dropping it from the other throws
> the two indices out of alignment.
