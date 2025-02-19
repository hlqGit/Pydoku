import random

def is_valid(board, row, col, num):
    """Checks if a number is valid in a sudoku board."""
    # If number exists in the row, num isn't valid
    if num in board[row]:
        return False
    
    # If number exists in the column, num isn't valid
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # If number exists in the 3x3 house it is in, num isn't valid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    # If num passes all checks, it is valid
    return True

def solve_for_sudoku(board, row=0, col=0):
    """Solves for a valid sudoku board recursively."""
    # If row is 9, the board has been solved for
    if row == 9:
        return True
    
    # If column is 9, move to the next row, otherwise move to the next column
    next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)
    
    # If the current cell isn't empty, move to the next cell
    if board[row][col] != 0:
        return solve_for_sudoku(board, next_row, next_col)
    
    # Shuffle the numbers 1-9 in a list
    nums = list(range(1, 10))
    random.shuffle(nums)

    # Check if each number would be valid in the cell
    for num in nums:
        # Until a valid number is found, keep checking the shuffled list
        if is_valid(board, row, col, num):
            board[row][col] = num
            # Once it has found a valid number, move to the next cell recursively
            if solve_for_sudoku(board, next_row, next_col):
                return True
            board[row][col] = 0
    
    return False

def generate_board():
    """Generates a nine by nine, two-dimensional list with numbers that make up a valid sudoku board."""
    # Create a nine by nine board with all zeros
    sudoku_board = [[0 for _ in range(9)] for _ in range(9)]
    # Solve for a valid sudoku board
    solve_for_sudoku(sudoku_board)
    # Return the solved board
    return sudoku_board

# If the file is run directly, print a generated board
if __name__ == "__main__":
    sudoku_board = generate_board()
    for row in sudoku_board:
        print(row)
