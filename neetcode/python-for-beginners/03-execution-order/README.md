# 3. Execution Order

**Difficulty:** Easy

[View on NeetCode](https://neetcode.io/courses/lessons/execution-order)

## Problem

In programming, code is generally executed line-by-line, from top to bottom, and
this holds true for Python code as well. This means that the order in which you
write your code is important.

For example, the following code:

```python
print("First")
print("Second")
print("Third")
```

will output:

```
First
Second
Third
```

## Challenge

In the code editor, there are three print statements. Rearrange them so that the
output is:

```
Fourth
Fifth
Sixth
```

If you think you have the correct answer, click the Submit button.

## Examples

**Example 1:**

```
Input: (none)
Output: Fourth
        Fifth
        Sixth
```

## Solution

See [`code.py`](code.py).

Statements run top to bottom, so ordering the `print` calls Fourth, Fifth, Sixth
produces the required output.

- **Time:** O(1)
- **Space:** O(1)
