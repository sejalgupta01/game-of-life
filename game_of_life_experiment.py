import pygame
import numpy as np

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Grid variables
cell_size = 20
grid_width, grid_height = screen_width // cell_size, screen_height // cell_size
grid = np.zeros((grid_width, grid_height), dtype=bool)

# Function to update the grid
def update_grid():
    new_grid = grid.copy()
    for x in range(grid_width):
        for y in range(grid_height):
            neighbors = count_live_neighbors(x, y)
            if grid[x, y]:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = False
            elif neighbors == 3:
                new_grid[x, y] = True
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

# Function to draw the grid
def draw_grid():
    screen.fill(BLACK)

    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x, y]:
                pygame.draw.rect(screen, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Main game loop
running = True
drawing = False
clearing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
            elif event.button == 3:  # Right mouse button
                clearing = True
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 1:  # Left mouse button
        #         drawing = False
        #     elif event.button == 3:  # Right mouse button
        #         clearing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Get user input for grid size
                input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 15, 200, 30)
                color_inactive = pygame.Color('lightskyblue3')
                color_active = pygame.Color('dodgerblue2')
                color = color_inactive
                user_input = ''
                active = True

                while active:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            running = False
                            active = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if input_box.collidepoint(event.pos):
                                active = True
                                color = color_active
                            else:
                                active = False
                                color = color_inactive
                        if event.type == pygame.KEYDOWN:
                            if active:
                                if event.key == pygame.K_RETURN:
                                    try:
                                        new_width, new_height = map(int, user_input.split())
                                        if new_width > 0 and new_height > 0:
                                            grid_width, grid_height = new_width, new_height
                                            grid = np.zeros((grid_width, grid_height), dtype=bool)
                                            cell_size = min(screen_width // grid_width, screen_height // grid_height)
                                            active = False
                                            color = color_inactive
                                            user_input = ''
                                            draw_grid()
                                    except ValueError:
                                        user_input = ''
                                elif event.key == pygame.K_BACKSPACE:
                                    user_input = user_input[:-1]
                                else:
                                    user_input += event.unicode

                    screen.fill(BLACK)
                    font = pygame.font.SysFont(None, 24)
                    txt_surface = font.render("Enter new grid size (width height): " + user_input, True, color)
                    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                    pygame.draw.rect(screen, color, input_box, 2)
                    pygame.display.flip()

    if drawing or clearing:
        x, y = pygame.mouse.get_pos()
        x = x // cell_size
        y = y // cell_size
        if 0 <= x < grid_width and 0 <= y < grid_height:
            grid[x, y] = drawing
            draw_grid()

    grid = update_grid()
    draw_grid()
    clock.tick(10)

pygame.quit()