import pygame
from typing import List
import random
from collections import deque

pygame.init()

# Setting up the display
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze-Generator")

# Constants
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (0, 0, 0)

# Maze walls representation
maze_walls = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
# 0 - up, 1 - right, 2 - down, 3 - left 

# directions
dir_x = [-1, 0, 1, 0]
dir_y = [0, 1, 0, -1]
directions = list(range(4))

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH + 1, CELL_SIZE):
        pygame.draw.line(SCREEN, BLUE, (x, 0), (x, HEIGHT), width=2)
    for y in range(0, HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(SCREEN, BLUE, (0, y), (WIDTH, y), width=2)

# Function to check if a coordinates are valid
def isValid(i: int, j: int) -> bool:
    if i < 0 or i >= ROWS or j < 0 or j >= COLS:
        return False
    return True

# Function to check if a move can be made in a given direction
def can_move(i: int, j: int, direction: int):
    return not maze_walls[i][j][direction]

# Function to generate the maze (I'm using simple-DFS)
def generate_maze(visited: List[List[bool]], coord: tuple[int, int], walls_removed: List[tuple]):
    i, j = coord
    visited[i][j] = True
    random.shuffle(directions)

    for k in directions:
        new_i = i + dir_x[k]
        new_j = j + dir_y[k]

        if not isValid(new_i, new_j) or visited[new_i][new_j]:
            continue

        if new_i == i and new_j == j + 1:
            start = ((j + 1) * CELL_SIZE, i * CELL_SIZE)
            end = ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE)
            maze_walls[i][j][1] = False
            maze_walls[new_i][new_j][3] = False
            
        elif new_i == i and new_j == j - 1:
            start = (j * CELL_SIZE, i * CELL_SIZE)
            end = (j * CELL_SIZE, (i + 1) * CELL_SIZE)
            maze_walls[i][j][3] = False
            maze_walls[new_i][new_j][1] = False
            
        elif new_i == i - 1 and new_j == j:
            start = (j * CELL_SIZE, i * CELL_SIZE)
            end = ((j + 1) * CELL_SIZE, i * CELL_SIZE)
            maze_walls[i][j][0] = False
            maze_walls[new_i][new_j][2] = False
            
        elif new_i == i + 1 and new_j == j:
            start = (j * CELL_SIZE, (i + 1) * CELL_SIZE)
            end = ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE)
            maze_walls[i][j][2] = False
            maze_walls[new_i][new_j][0] = False

        walls_removed.append((start, end))
        generate_maze(visited, (new_i, new_j), walls_removed)


# Function to find the furthest boundary cell from a given start cell (Doing a BFS)
def find_furthest_boundary_cell(start_i: int, start_j: int) -> tuple[int, int]:
    visited = [[False] * COLS for _ in range(ROWS)]
    dist = [[-1] * COLS for _ in range(ROWS)]
    queue = deque()
    queue.append((start_i, start_j))
    visited[start_i][start_j] = True
    dist[start_i][start_j] = 0
    max_dist = 0
    end = (start_i, start_j)

    while queue:
        i, j = queue.popleft()
        for d in range(4):
            if can_move(i, j, d):
                ni = i + dir_x[d]
                nj = j + dir_y[d]
                if isValid(ni, nj) and not visited[ni][nj]:
                    visited[ni][nj] = True
                    dist[ni][nj] = dist[i][j] + 1
                    queue.append((ni, nj))
                    if dist[ni][nj] > max_dist:
                        max_dist = dist[ni][nj]
                        end = (ni, nj)
    return end


def main():
    pygame.font.init()
    font = pygame.font.SysFont("arial", 30)

    game_running = True
    game_state = 0
    walls_removed = []
    start_coord = [0] * 2
    end_coord = [0] * 2
    cur_i = 0
    cur_j = 0
    visited = [[False] * COLS for _ in range(ROWS)]
    clock = pygame.time.Clock()

    while game_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if game_state == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    i = event.pos[1] // CELL_SIZE
                    j = event.pos[0] // CELL_SIZE
                    cur_i = i
                    cur_j = j
                    start_coord[0] = j * CELL_SIZE + (CELL_SIZE / 2)
                    start_coord[1] = i * CELL_SIZE + (CELL_SIZE / 2)

                    generate_maze(visited, (i, j), walls_removed)
                    end_i, end_j = find_furthest_boundary_cell(i, j)
                    end_coord[0] = end_j * CELL_SIZE + (CELL_SIZE / 2)
                    end_coord[1] = end_i * CELL_SIZE + (CELL_SIZE / 2)

                    game_state = 1

            if game_state == 1:
                if event.type == pygame.KEYDOWN:
                    game_state = 2

            if game_state == 2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if can_move(cur_i, cur_j, 3):
                            cur_j -= 1
                            start_coord[0] -= CELL_SIZE
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if can_move(cur_i, cur_j, 1):
                            cur_j += 1
                            start_coord[0] += CELL_SIZE
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if can_move(cur_i, cur_j, 0):
                            cur_i -= 1
                            start_coord[1] -= CELL_SIZE
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if can_move(cur_i, cur_j, 2):
                            cur_i += 1
                            start_coord[1] += CELL_SIZE

        SCREEN.fill(BG_COLOR)
        draw_grid()

        for start, end in walls_removed:
            
            pygame.draw.line(SCREEN, BG_COLOR, start, end, width=2)

        
        if game_state >= 1:
            pygame.draw.circle(SCREEN, GREEN, start_coord, 5)
            pygame.draw.circle(SCREEN, RED, end_coord, 5)
            
        if game_state == 1:
            message = font.render("Start Your Game!!! (Press any key)", True, GREEN)
            SCREEN.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()