# 4. Printing Text

**Difficulty:** Easy

[View on NeetCode](https://neetcode.io/courses/lessons/printing-text)

## Problem

The `print()` function writes text to the output. The text you want to print goes
inside the parentheses, wrapped in quotes:

```python
print("Hello, world!")
```

Text wrapped in quotes is called a **string**. A string can be written with double
quotes (`"..."`) or single quotes (`'...'`) — both work the same way.

This matters when the text itself contains a quote character. If you write a double
quote inside a double-quoted string, Python thinks the string has ended early and
the code breaks. There are two ways around this:

- Use the other quote style on the outside: `print('She said "hi"')`
- **Escape** the inner quotes with a backslash: `print("She said \"hi\"")`

## Challenge

Print the following line of text, including the double quotes around the quotation:

```
My favorite quote is "To be or not to be."
```

**Hint:** The backslash (`\`) tells Python to treat the next character as part of
the string rather than as the end of it.

## Examples

**Example 1:**

```
Input: (none)
Output: My favorite quote is "To be or not to be."
```

## Solution

See [`code.py`](code.py).

Escape each inner double quote with a backslash so Python reads them as characters
in the string instead of as the string's closing delimiter.

- **Time:** O(1)
- **Space:** O(1)
