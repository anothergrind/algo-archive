# 36. Valid Sudoku

**Difficulty:** Medium

[View on LeetCode](https://leetcode.com/problems/valid-sudoku/)

## Problem

You are given a 9 x 9 Sudoku board. A Sudoku board is valid if the following rules are
followed:

- Each row must contain the digits `1-9` without duplicates.
- Each column must contain the digits `1-9` without duplicates.
- Each of the nine 3 x 3 sub-boxes of the grid must contain the digits `1-9` without
  duplicates.

Return `true` if the Sudoku board is valid, otherwise return `false`.

**Note:** a board does not need to be full or be solvable to be valid.

## Examples

**Example 1:**

```
Input: board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","8",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]
Output: true
```

**Example 2:**

```
Input: board =
[["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","1",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: the top-left 3x3 sub-box contains two 1s.
```

## Solution

See [`code.py`](code.py).

Three separate passes, each using a fresh set to detect a repeat: one over the rows,
one over the columns, and one over the nine 3 x 3 sub-boxes.

- **Time:** O(n^2) over the 9 x 9 board
- **Space:** O(n) for the per-group set
