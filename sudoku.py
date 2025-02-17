# Example file showing a circle moving on screen
import pygame
import random
from generate_board import generate_board

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 800))
running = True
clock = pygame.time.Clock()
selected_square = None
user_input_squares = []
pygame.display.set_caption("Sudoku")
won = False

key = generate_board()
board = [row.copy() for row in key]

# Select difficulty and remove corresponding number of squares
EASY = 50
MEDIUM = 60
HARD = 70
# user input and and make sure user input is an integer between 1 and 3
difficulty = int(input("Enter a number for the difficulty level: 1. Easy, 2. Medium, or 3. Hard: "))
while difficulty not in [1, 2, 3]:
    difficulty = int(input("Enter a number for the difficulty level: 1. Easy, 2. Medium, or 3. Hard: "))
match difficulty:
    case 1:
        remove = EASY
    case 2:
        remove = MEDIUM
    case 3:
        remove = HARD
for _ in range(remove):
    i, j = random.randint(0, 8), random.randint(0, 8)
    board[i][j] = 0

# Uncomment to print key
# for elem in key:
#     print(elem)

while running:

    # ---------- EVENT HANDLING ---------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
    if won:
        screen.fill("darkslategrey")
    else: screen.fill("white")

    # ---------- DRAW GRID ---------- #
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, "black", (i * 80, 0), (i * 80, 720), 4)
            pygame.draw.line(screen, "black", (0, i * 80), (720, i * 80), 4)
        else:
            pygame.draw.line(screen, "black", (i * 80, 0), (i * 80, 720), 2)
            pygame.draw.line(screen, "black", (0, i * 80), (720, i * 80), 2)
    x, y = pygame.mouse.get_pos()
    i, j = x // 80, y // 80
    if i < 9 and j < 9:
        pygame.draw.rect(screen, "darkblue", (i * 80, j * 80, 80, 80), 3)

    # ---------- SELECT SQUARE ---------- #
    if pygame.mouse.get_pressed()[0]:
        if i < 9 and j < 9:
            selected_square = (i, j)

    # ---------- HIGHLIGHT SELECTED SQUARE ---------- #
    if selected_square is not None and not won:
        i, j = selected_square
        if board[j][i] != 0 and selected_square not in user_input_squares:
            selected_square = None
        pygame.draw.rect(screen, "lightblue", ((i * 80) + 2, (j * 80) + 2, 77, 77))

    # ---------- DRAW BOARD NUMBERS ---------- #
    for i in range(9):
        for j in range(9):
            # if won, display all numbers in green
            if won:
                font = pygame.font.Font(None, 36)
                if (i, j) in user_input_squares:
                    text = font.render(str(board[j][i]), True, "green")
                else: 
                    text = font.render(str(key[j][i]), True, "lightblue")
                text_rect = text.get_rect(center=(i * 80 + 40, j * 80 + 40))
                screen.blit(text, text_rect)
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
            if selected_square is not None:
                x, y = selected_square
                board[y][x] = i
                selected_square = None
                user_input_squares.append((x, y))

    # ---------- CLEAR NUMBER ---------- #
    if keys[pygame.K_BACKSPACE]:
        if selected_square is not None:
            x, y = selected_square
            board[y][x] = 0
            if (x, y) in user_input_squares:
                user_input_squares.remove((x, y))
            selected_square = None

    # ---------- DESELECT SQUARE ---------- #
    if keys[pygame.K_SPACE]:
        selected_square = None

    # ---------- HOLD TO CHECK BOARD ---------- #
    if keys[pygame.K_v]:
        for i in range(9):
            for j in range(9):
                if board[j][i] != 0 and (i, j) in user_input_squares:
                    if board[j][i] == key[j][i]:
                        color = "green"
                    else:
                        color = "red"
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[j][i]), True, color)
                    text_rect = text.get_rect(center=(i * 80 + 40, j * 80 + 40))
                    screen.blit(text, text_rect)

    # ---------- CHECK IF WON ---------- #
    if all(all(row) for row in board):
        if all(board[j][i] == key[j][i] for i in range(9) for j in range(9)):
            won = True
    
    # Draw timer at bottom of screen
    font = pygame.font.Font(None, 36)
    text = font.render("Timer:", True, "black")
    text_rect = text.get_rect(center=(330, 760))
    screen.blit(text, text_rect)

    # ---------- TIMER ---------- #
    if not won:
        win_num = round(pygame.time.get_ticks() / 1000, 4)
        seconds = round(win_num, 1)
    else: seconds = win_num
    text = font.render(str(seconds), True, "black")
    text_rect = text.get_rect(left=375, centery=760)
    screen.blit(text, text_rect)

    # ---------- UPDATE SCREEN ---------- #
    pygame.display.flip()
    clock.tick(60)

pygame.quit()