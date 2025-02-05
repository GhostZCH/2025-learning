import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# 定义屏幕大小和格子大小
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# 初始化字体
font = pygame.font.SysFont("comicsans", 40)

# 初始化游戏板
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def add_new_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def draw_board():
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            color = COLORS.get(value, WHITE)
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def move_left():
    new_board = []
    for row in board:
        new_row = [cell for cell in row if cell != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        for i in range(GRID_SIZE - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [cell for cell in new_row if cell != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        new_board.append(new_row)
    return new_board

def move_right():
    new_board = []
    for row in board:
        new_row = [cell for cell in row if cell != 0]
        new_row = [0] * (GRID_SIZE - len(new_row)) + new_row
        for i in range(GRID_SIZE - 1, 0, -1):
            if new_row[i] == new_row[i - 1]:
                new_row[i] *= 2
                new_row[i - 1] = 0
        new_row = [cell for cell in new_row if cell != 0]
        new_row = [0] * (GRID_SIZE - len(new_row)) + new_row
        new_board.append(new_row)
    return new_board

def move_up():
    new_board = [[board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    new_board = move_left()
    new_board = [[new_board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    return new_board

def move_down():
    new_board = [[board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    new_board = move_right()
    new_board = [[new_board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    return new_board

def is_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
    return True

# 初始化游戏
add_new_tile()
add_new_tile()

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_board = move_left()
            elif event.key == pygame.K_RIGHT:
                new_board = move_right()
            elif event.key == pygame.K_UP:
                new_board = move_up()
            elif event.key == pygame.K_DOWN:
                new_board = move_down()
            else:
                continue

            if new_board != board:
                board = new_board
                add_new_tile()
                if is_game_over():
                    print("Game Over!")
                    running = False

    draw_board()
    pygame.display.flip()

pygame.quit()