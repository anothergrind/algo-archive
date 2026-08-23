# Delivery Delay Risk Scores

## Problem

> The original prompt text is not stored in this repo. The statement below was
> reconstructed from the solution and the author's notes — paste the real prompt over
> it when convenient.

Given a list of integer `delivery_offsets` sorted in non-decreasing order, return a
list of the square of each offset, also sorted in non-decreasing order.

Offsets may be negative, so the largest risk scores can come from either end of the
input.

## Examples

Verified by running [`code.py`](code.py):

**Example 1:**

```
Input: delivery_offsets = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: squaring gives [16,1,0,9,100], which sorts to [0,1,9,16,100].
```

**Example 2:**

```
Input: delivery_offsets = [-7,-3,2,3,11]
Output: [4,9,9,49,121]
```

## Solution

See [`code.py`](code.py).

Two pointers, one at each end of the sorted input. Whichever end squares to the larger
value is written into the back of the result, and that pointer steps inward. Because
the input is sorted, the largest square is always at one end or the other, so the
result fills correctly from the back without a sort.

- **Time:** O(n)
- **Space:** O(n) for the output

> This is a themed version of what is otherwise the classic "squares of a sorted array"
> problem.
