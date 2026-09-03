# 5. Code Errors

**Difficulty:** Easy

[View on NeetCode](https://neetcode.io/courses/lessons/code-errors)

## Problem

Earlier, if you attempted to run the following code before correcting it:

```python
print("My favorite quote is "To be or not to be."")
```

You may have seen something like this in the console:

```
ERROR!
Traceback (most recent call last):
  File "<main.py>", line 1
    print("My favorite quote is "To be or not to be."")
          ^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

This is the result of an error in our code. Specifically, it's a **syntax error**.
Syntax errors occur when the code is not written correctly according to the rules of
the programming language. It's not so different from a spelling or grammar error in
a human language, except that computers are much less forgiving.

Sometimes you may get helpful error messages which help you identify the problem.
Other times, the error message may not be as clear.

There are many types of programming errors such as syntax errors, runtime errors,
and logical errors. Syntax errors are easier to fix, because they usually point out
which line the error is on.

## Challenge

In the code editor, there is a syntax error. Correct the code so that it prints the
following text to the console:

```
Can someone pls add a closing parenthesis?
```

## Examples

**Example 1:**

```
Input: (none)
Output: Can someone pls add a closing parenthesis?
```

## Solution

See [`code.py`](code.py).

Close the `print` call with a matching parenthesis so the statement is valid syntax.

- **Time:** O(1)
- **Space:** O(1)
