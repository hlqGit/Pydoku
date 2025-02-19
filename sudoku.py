import pygame
import random
from generate_board import generate_board

# Generates a valid sudoku board as the key
key = generate_board()
# Copies the key to create the board
board = [row.copy() for row in key]

# Constants for difficulty levels
EASY = 45
MEDIUM = 55
HARD = 65

# get user input for difficulty and and make sure user input is an integer between 1 and 3
difficulty = int(input("Enter a number for the difficulty level: 1. Easy, 2. Medium, or 3. Hard: "))
while difficulty not in [1, 2, 3]:
    difficulty = int(input("Enter a number for the difficulty level: 1. Easy, 2. Medium, or 3. Hard: "))

# determine how many numbers to remove based on user-entered difficulty
match difficulty:
    case 1:
        remove = EASY
    case 2:
        remove = MEDIUM
    case 3:
        remove = HARD

# remove numbers from the board to create the puzzle
for _ in range(remove):
    i, j = random.randint(0, 8), random.randint(0, 8)
    board[i][j] = 0

# Uncomment to print key
# for elem in key:
#     print(elem)

# Initialize pygame and declare title and size of window
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 800))
pygame.display.set_caption("Sudoku")

# Initialize variables used in the loop
running = True
selected_square = None
user_input_squares = []
won = False

# Main loop
while running:

    # ---------- HANDLE X PRESS ---------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ## ---------- DRAW BACKGROUND ---------- #
    if won:
        screen.fill("darkslategrey")
    else: 
        screen.fill("white")

    # ---------- DRAW GRID ---------- #
    for i in range(10):
        # Draw thicker lines for every third line
        if i % 3 == 0:
            pygame.draw.line(screen, "black", (i * 80, 0), (i * 80, 720), 4)
            pygame.draw.line(screen, "black", (0, i * 80), (720, i * 80), 4)
        else:
            pygame.draw.line(screen, "black", (i * 80, 0), (i * 80, 720), 2)
            pygame.draw.line(screen, "black", (0, i * 80), (720, i * 80), 2)

    # ---------- HOVER EFFECT ---------- #
    x, y = pygame.mouse.get_pos()
    i, j = x // 80, y // 80
    if i < 9 and j < 9:
        pygame.draw.rect(screen, "darkblue", (i * 80, j * 80, 80, 80), 3)

    # ---------- USER SELECT SQUARE ---------- #
    if pygame.mouse.get_pressed()[0]:
        # ensure user is clicking within bounds (not on timer or anywhere else)
        if i < 9 and j < 9:
            selected_square = (i, j)

    # ---------- HIGHLIGHT SELECTED SQUARE ---------- #
    if selected_square is not None and not won:
        i, j = selected_square
        # Cannot select a square if the user did not input the number in the square.
        # User can select if empty square.
        if board[j][i] != 0 and selected_square not in user_input_squares:
            selected_square = None
        if selected_square is not None:
            pygame.draw.rect(screen, "lightblue", ((i * 80) + 2, (j * 80) + 2, 77, 77))

    # ---------- DRAW BOARD NUMBERS ---------- #
    for i in range(9):
        for j in range(9):
            # if user won, display user inputted numbers in green and pre-generated numbers as lightblue
            if won:
                font = pygame.font.Font(None, 36)
                if (i, j) in user_input_squares:
                    text = font.render(str(board[j][i]), True, "green")
                else: 
                    text = font.render(str(key[j][i]), True, "lightblue")
                text_rect = text.get_rect(center=(i * 80 + 40, j * 80 + 40))
                screen.blit(text, text_rect)
            # if user has not won, display user inputted numbers in blue and pre-generated numbers in black
            elif board[j][i] != 0:
                font = pygame.font.Font(None, 36)
                if (i, j) in user_input_squares:
                    text = font.render(str(board[j][i]), True, "blue")
                else:
                    text = font.render(str(board[j][i]), True, "black")
                text_rect = text.get_rect(center=(i * 80 + 40, j * 80 + 40))
                screen.blit(text, text_rect)

    # ---------- USER INPUT NUMBER ---------- #
    keys = pygame.key.get_pressed()
    for i in range(1, 10):
        if keys[pygame.K_0 + i]:
            # ensure user has selected a square before inputting a number
            if selected_square is not None:
                x, y = selected_square
                board[y][x] = i
                user_input_squares.append((x, y))

    # ---------- CLEAR NUMBER ---------- #
    if keys[pygame.K_BACKSPACE]:
        # ensure user has selected a square before clearing a number
        if selected_square is not None:
            x, y = selected_square
            # clears number and removes square from user_input_squares
            board[y][x] = 0
            if (x, y) in user_input_squares:
                user_input_squares.remove((x, y))

    # ---------- DESELECT SQUARE ---------- #
    if keys[pygame.K_SPACE]:
        selected_square = None

    # ---------- HOLD TO CHECK BOARD ---------- #
    if keys[pygame.K_v]:
        for i in range(9):
            for j in range(9):
                # Only highlight user inputted numbers
                if board[j][i] != 0 and (i, j) in user_input_squares:
                    # If number is correct, highlight in green, else highlight in red
                    if board[j][i] == key[j][i]:
                        color = "green"
                    else:
                        color = "red"
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[j][i]), True, color)
                    text_rect = text.get_rect(center=(i * 80 + 40, j * 80 + 40))
                    screen.blit(text, text_rect)

    # ---------- CHECK IF WON ---------- #
    # Checks if all of the sqaures on the board match the key generated earlier
    if all(all(row) for row in board):
        if all(board[j][i] == key[j][i] for i in range(9) for j in range(9)):
            won = True
    
    # Draw timer at bottom of screen
    font = pygame.font.Font(None, 36)
    text = font.render("Timer:", True, "black")
    text_rect = text.get_rect(center=(330, 760))
    screen.blit(text, text_rect)

    # ---------- TIMER ---------- #
    # will display the time with 1 decimal place if the user hasn't won yet
    if not won:
        win_num = round(pygame.time.get_ticks() / 1000, 4)
        seconds = round(win_num, 1)
    else: 
        # will display the time withm 3 decimal places if the user has won
        seconds = win_num
    text = font.render(str(seconds), True, "black")
    text_rect = text.get_rect(left=375, centery=760)
    screen.blit(text, text_rect)

    # ---------- UPDATE SCREEN ---------- #
    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()