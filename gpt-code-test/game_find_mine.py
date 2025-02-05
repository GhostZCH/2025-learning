import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 定义屏幕大小和格子大小
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# 初始化字体
font = pygame.font.SysFont("comicsans", 20)

# 初始化游戏板
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mines = set()

# 随机放置地雷
NUM_MINES = 15
while len(mines) < NUM_MINES:
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    mines.add((x, y))
    board[x][y] = -1

# 计算每个格子周围的地雷数量
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if board[x][y] == -1:
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE and board[x + dx][y + dy] == -1:
                    board[x][y] += 1

def draw_board():
    screen.fill(WHITE)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if revealed[x][y]:
                if board[x][y] == -1:
                    pygame.draw.rect(screen, RED, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, GRAY, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    if board[x][y] > 0:
                        text = font.render(str(board[x][y]), True, BLACK)
                        text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLACK, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def reveal(x, y):
    if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
        return
    if revealed[x][y]:
        return
    revealed[x][y] = True
    if board[x][y] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                reveal(x + dx, y + dy)

def check_win():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] != -1 and not revealed[x][y]:
                return False
    return True

# 游戏主循环
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            x //= CELL_SIZE
            y //= CELL_SIZE
            if board[y][x] == -1:
                game_over = True
                print("Game Over!")
            else:
                reveal(y, x)
                if check_win():
                    game_over = True
                    print("You Win!")

    draw_board()
    pygame.display.flip()

pygame.quit()