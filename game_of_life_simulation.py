import pygame
import numpy as np

DEFAULT_GRID_SIZE = WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
DEFAULT_GRID_WIDTH = 60
DEFAULT_GRID_HEIGHT = 50

pygame.init()
screen = pygame.display.set_mode(DEFAULT_GRID_SIZE)

grid_width = DEFAULT_GRID_WIDTH
grid_height = DEFAULT_GRID_HEIGHT
grid = np.zeros((grid_width, grid_height), dtype=bool)
generation = 0
population = 0

def update_grid():
    global generation, population
    generation += 1
    new_grid = np.copy(grid)
    for x in range(grid_width):
        for y in range(grid_height):
            neighbors = count_live_neighbors(x, y)
            if grid[x, y]:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = False
            elif neighbors == 3:
                new_grid[x, y] = True
    population = sum([sum(row) for row in new_grid])
    return new_grid

def count_live_neighbors(x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % grid_width
            ny = (y + dy) % grid_height
            if grid[nx, ny]:
                count += 1
    return count

def draw_grid():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), grid_rect)
    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x, y]:
                rect = pygame.Rect(left_margin + x * CELL_SIZE, top_margin + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect)

def handle_next_button_click():
    global grid
    grid = update_grid()

def handle_populate_button_click():
    global grid, generation, population
    generation = 0
    grid = np.random.choice([True, False], (grid_width, grid_height), p=[0.2, 0.8])
    population = sum([sum(row) for row in grid])

def handle_clear_button_click():
    global grid, generation, population
    generation = 0
    population = 0
    grid = np.zeros((grid_width, grid_height), dtype=bool)

def handle_cell_click(x, y):
    global generation, population
    generation = 0
    grid[x, y] = not grid[x, y]
    if grid[x, y]:
        population += 1
    else:
        population -= 1

# Grid properties
left_margin = (WIDTH - grid_width * CELL_SIZE) // 2
top_margin = (HEIGHT - grid_height * CELL_SIZE) // 4
grid_rect = pygame.Rect(left_margin, top_margin, grid_width * CELL_SIZE, grid_height * CELL_SIZE)

# Button properties
button_width = 150
button_height = 50
button_font = pygame.font.SysFont(None, 35)
button_color = (0, 255, 0)

# Top row button properties
top_row_button_top = HEIGHT - 175

# Bottom row button properties
bottom_row_button_top = HEIGHT - 100

# Populate button
populate_button_left = (WIDTH - (100 + button_width * 3)) // 2
populate_button_rect = pygame.Rect(populate_button_left, top_row_button_top, button_width, button_height)
populate_button_text = button_font.render("Populate", True, (0, 0, 0))

# Clear button
clear_button_left = populate_button_left + button_width + 50
clear_button_rect = pygame.Rect(clear_button_left, top_row_button_top, button_width, button_height)
clear_button_text = button_font.render("Clear", True, (0, 0, 0))

# Next button
next_button_left = clear_button_left + button_width + 50
next_button_rect = pygame.Rect(next_button_left, top_row_button_top, button_width, button_height)
next_button_text = button_font.render("Next", True, (0, 0, 0))

running = True
paused = True
clock = pygame.time.Clock()

while running:
    clock.tick(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if next_button_rect.collidepoint(event.pos):
                    handle_next_button_click()
                elif populate_button_rect.collidepoint(event.pos):
                    handle_populate_button_click()
                elif clear_button_rect.collidepoint(event.pos):
                    handle_clear_button_click()
                elif grid_rect.collidepoint(event.pos):
                    cell_x = (event.pos[0] - left_margin) // CELL_SIZE
                    cell_y = (event.pos[1]  - top_margin) // CELL_SIZE
                    handle_cell_click(cell_x, cell_y)
        if not paused:
            grid = update_grid()

    draw_grid()

    # Generation text
    gen_text = button_font.render("Generation: " + str(generation), True, (255, 255, 255))
    screen.blit(gen_text, (left_margin, top_margin - gen_text.get_height() - 10))

    # Population text
    pop_text = button_font.render("Population: " + str(population), True, (255, 255, 255))
    screen.blit(pop_text, (left_margin + grid_width * CELL_SIZE - pop_text.get_width(), top_margin - gen_text.get_height() - 10))

    pygame.draw.rect(screen, button_color, populate_button_rect)
    screen.blit(populate_button_text, (populate_button_left + (button_width - populate_button_text.get_width()) // 2, top_row_button_top + (button_height - populate_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, clear_button_rect)
    screen.blit(clear_button_text, (clear_button_left + (button_width - clear_button_text.get_width()) // 2, top_row_button_top + (button_height - clear_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, next_button_rect)
    screen.blit(next_button_text, (next_button_left + (button_width - next_button_text.get_width()) // 2, top_row_button_top + (button_height - next_button_text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()