# You are given a 9 x 9 Sudoku board board. A Sudoku board is valid if the following rules are followed:
#     Each row must contain the digits 1-9 without duplicates.
#     Each column must contain the digits 1-9 without duplicates.
#     Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without duplicates.

# Return true if the Sudoku board is valid, otherwise return false
# Note: A board does not need to be full or be solvable to be valid.

# Example #1
# Input: board =
# [["1","2",".",".","3",".",".",".","."],
#  ["4",".",".","5",".",".",".",".","."],
#  [".","9","8",".",".",".",".",".","3"],
#  ["5",".",".",".","6",".",".",".","4"],
#  [".",".",".","8",".","3",".",".","5"],
#  ["7",".",".",".","2",".",".",".","6"],
#  [".",".",".",".",".",".","2",".","."],
#  [".",".",".","4","1","9",".",".","8"],
#  [".",".",".",".","8",".",".","7","9"]]
# Output: true

# Example 2
# Input: board =
# [["1","2",".",".","3",".",".",".","."],
#  ["4",".",".","5",".",".",".",".","."],
#  [".","9","1",".",".",".",".",".","3"],
#  ["5",".",".",".","6",".",".",".","4"],
#  [".",".",".","8",".","3",".",".","5"],
#  ["7",".",".",".","2",".",".",".","6"],
#  [".",".",".",".",".",".","2",".","."],
#  [".",".",".","4","1","9",".",".","8"],
#  [".",".",".",".","8",".",".","7","9"]]

# Output: false

def isValidSudoku(self, board: list[list[str]]) -> bool:
    # Algorithm Analysis - Time: O(n^2), space: O(n)

    # Psuedocode: 
    # let's treat i as rows and j as columns
    # we want to iterate through all the rows and columns 

    # solving the problem like psuedocode
    #   iterate through the rows, and check if there's more than one occurance of a number
    #   iterate through the columns, and check if there's more than one occurance of a number
    # 
    #   iterate through the first 3x3 box, check if there's more than one occurance (shift right)
    #       repeat this twice for the other 3x3 on the first block of boxes (shift right)
    #   iterate through the second 3x3 box, check if there's more than one occurance (shift right)
    #       repeat this twice for the other 3x3 on the second block of boxes (shift right)
    #   iterate through the third 3x3 box, check if there's more than one occurance (shift right)
    #       repeat this twice for the other 3x3 on the third block of boxes (shift right)

    # if at any time that there's more occurance of a number, return false
    # if you make it through all iterations, return true

    for i in range(9):
        row_set = set()
        for j in range(9):
            num = board[i][j]
            if num != '.':
                if num in row_set:
                    return False
                row_set.add(num)

    for j in range(9):
        col_set = set()
        for i in range(9):
            num = board[i][j]
            if num != '.':
                if num in col_set:
                    return False
                col_set.add(num)


    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            box_set = set()
            for di in range(3):
                for dj in range(3):
                    num = board[block_row + di][block_col + dj]
                    if num != '.':
                        if num in box_set:
                            return False
                        box_set.add(num)
    
    return True       