# Decode a Lab Diagnostic Code

## Problem

> The original prompt text is not stored in this repo. The statement below was
> reconstructed from the solution and the author's notes — paste the real prompt over
> it when convenient.

A diagnostic code is written using the characters `I`, `V`, `X`, `L`, `C`, `D` and `M`,
which stand for the following values:

| Symbol | Value |
| ------ | ----- |
| `I`    | 1     |
| `V`    | 5     |
| `X`    | 10    |
| `L`    | 50    |
| `C`    | 100   |
| `D`    | 500   |
| `M`    | 1000  |

Values are normally written largest to smallest and added together. When a smaller
value appears immediately before a larger one, it is subtracted instead — so `IX` is
9, not 11.

Given a diagnostic code as a string, return its integer value.

## Examples

Verified by running [`code.py`](code.py):

**Example 1:**

```
Input: diagnostic_code = "III"
Output: 3
```

**Example 2:**

```
Input: diagnostic_code = "LVIII"
Output: 58
Explanation: L = 50, V = 5, III = 3.
```

**Example 3:**

```
Input: diagnostic_code = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90, IV = 4.
```

## Solution

See [`code.py`](code.py).

Walks the string comparing each character to the one after it. If the next value is
larger, the current one is subtracted; otherwise it is added. The final character has
no successor to compare against, so it is always added at the end.

- **Time:** O(n)
- **Space:** O(1)

> This is a themed version of what is otherwise the classic Roman numeral to integer
> conversion.
