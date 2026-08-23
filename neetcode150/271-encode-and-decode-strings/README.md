# 271. Encode and Decode Strings

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/encode-and-decode-strings/) (premium)

## Problem

Design an algorithm to encode a list of strings to a single string. The encoded string
is then sent over the network and decoded back to the original list of strings.

Machine 1 (sender) does:

```
string encoded_string = encode(strs);
```

Machine 2 (receiver) does:

```
vector<string> strs2 = decode(encoded_string);
```

`strs2` on Machine 2 should be the same as `strs` on Machine 1.

## Examples

**Example 1:**

```
Input: dummy_input = ["Hello","World"]
Output: ["Hello","World"]
```

**Example 2:**

```
Input: dummy_input = [""]
Output: [""]
```

## Constraints

- `0 <= strs.length < 100`
- `0 <= strs[i].length < 200`
- `strs[i]` contains any possible characters out of 256 valid ASCII characters.

## Solution

See [`code.py`](code.py).

`encode` joins the list with a space separator; `decode` walks the string and splits on
spaces, skipping empty runs.

> **Note:** the space separator is not safe for this problem. The constraints allow any
> ASCII character, so a string that itself contains a space will be split into two
> entries on decode, and empty strings in the middle of the list are lost. The standard
> fix is length-prefixed encoding: write `len(s)` then a delimiter then `s` for each
> string, so the decoder reads exactly that many characters and never has to guess.
