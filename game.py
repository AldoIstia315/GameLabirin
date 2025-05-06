import pygame
import random
import sys


TILE_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 25


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


maze = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def in_bounds(x, y):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

def generate_maze(x, y):
    maze[y][x] = 0
    directions = DIRS[:]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx*2, y + dy*2
        if in_bounds(nx, ny) and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            generate_maze(nx, ny)


generate_maze(1,1)


start = (1, 1)
end = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
maze[end[1]][end[0]] = 0 


pygame.init()
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirin Acak dengan Jalan Keluar")

player_pos = list(start)
clock = pygame.time.Clock()

def draw_maze():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, rect)

def draw_player():
    rect = pygame.Rect(player_pos[0]*TILE_SIZE, player_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, rect)

def draw_goal():
    rect = pygame.Rect(end[0]*TILE_SIZE, end[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, GREEN, rect)


running = True
while running:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    x, y = player_pos
    if keys[pygame.K_LEFT] and maze[y][x - 1] == 0:
        player_pos[0] -= 1
    elif keys[pygame.K_RIGHT] and maze[y][x + 1] == 0:
        player_pos[0] += 1
    elif keys[pygame.K_UP] and maze[y - 1][x] == 0:
        player_pos[1] -= 1
    elif keys[pygame.K_DOWN] and maze[y + 1][x] == 0:
        player_pos[1] += 1

    # Cek kemenangan
    if tuple(player_pos) == end:
        print("Victory")
        pygame.quit()
        sys.exit()

    # Gambar ulang layar
    screen.fill(WHITE)
    draw_maze()
    draw_goal()
    draw_player()
    pygame.display.flip()
