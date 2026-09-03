# 2. What is Python?

**Difficulty:** Easy

[View on NeetCode](https://neetcode.io/courses/lessons/what-is-python)

## Problem

Python is an interpreted programming language. It was created by Guido van Rossum
and first released in 1991. Python is known for its simplicity and readability,
which makes it a great language for beginners.

Python is one of the most popular languages in the world. It is often the preferred
language when automating tasks via scripts. It is also widely used in scientific
computing, data science, machine learning, and backend web development.

This course will teach you the core concepts of Python. But if you're a beginner,
the most important thing you will learn is how to think like a programmer.

## Challenge

You can click the Submit button to execute the code. Don't worry if you don't
understand any of it.

You will notice that the output is incorrect. We want to calculate the first 20
digits of pi, but right now our program is only printing the first 19 digits. With
the power of programming we can fix this by changing a single line of code.

To fix this, find the following line of code:

```python
n = 19
```

and change the number to 20. Then click the Submit button again.

**Hint:** If you don't want to read through the code, click the editor and press
`Ctrl + F`. You can then type `n = 19` to find the line of code you need to change.

## Examples

**Example 1:**

```
Input: (none)
Output: 3.1415926535897932384
```

**Example 2:**

```
Input: (none)
Output: 3.14159265358979323846
```

## Solution

See [`code.py`](code.py).

The Chudnovsky algorithm computes pi to arbitrary precision; `n` controls how many
digits are produced. Changing `n` from 19 to 20 yields the extra digit.

- **Time:** O(n)
- **Space:** O(n)
