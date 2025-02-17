import random

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    
    if num in [board[i][col] for i in range(9)]:
        return False
    
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def solve_sudoku(board, row=0, col=0):
    if row == 9:
        return True
    
    next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)
    
    if board[row][col] != 0:
        return solve_sudoku(board, next_row, next_col)
    
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board, next_row, next_col):
                return True
            board[row][col] = 0
    
    return False

def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    return board

if __name__ == "__main__":
    sudoku_board = generate_board()
    for row in sudoku_board:
        print(row)
