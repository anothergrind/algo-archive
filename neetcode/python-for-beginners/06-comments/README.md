# 6. Comments

**Difficulty:** Easy

[View on NeetCode](https://neetcode.io/courses/lessons/comments)

## Problem

In programming we can annotate our code without affecting the output. This is done
using **comments**.

Comments are ignored by the interpreter. They are used to explain what the code is
doing or add any sort of message, usually for humans. They are useful for other
programmers who may read your code, or for yourself in the future if you forget what
a certain piece of code does.

In Python, comments are created using the `#` character. Any text after the `#`
character on a line is considered a comment.

```python
# This is a comment
```

If we want to ignore a piece of code, we can also comment it out temporarily. This
is useful for debugging or testing.

```python
# print("This line of code is commented out")
```

The above code will not print anything to the console because the line is commented
out.

## Challenge

Your task is to fix the code without deleting any of the lines. It should print the
following text to the console:

```
I belong here.
I also belong here.
Me too!
```

## Examples

**Example 1:**

```
Input: (none)
Output: I belong here.
        I also belong here.
        Me too!
```

## Solution

See [`code.py`](code.py).

Comment out the two unwanted `print` calls with `#` so the interpreter skips them,
leaving the three wanted lines to run.

- **Time:** O(1)
- **Space:** O(1)
