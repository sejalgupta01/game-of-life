import pygame
import numpy as np

DEFAULT_GRID_SIZE = WIDTH, HEIGHT = 800, 800
DEFAULT_CELL_SIZE = 10
DEFAULT_GRID_WIDTH = 60
DEFAULT_GRID_HEIGHT = 50

pygame.init()
screen = pygame.display.set_mode(DEFAULT_GRID_SIZE)

grid_width = DEFAULT_GRID_WIDTH
grid_height = DEFAULT_GRID_HEIGHT
cell_size = DEFAULT_CELL_SIZE
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
    global left_margin, top_margin, grid_rect
    screen.fill((0, 0, 0))
    left_margin = (WIDTH - grid_width * cell_size) // 2
    top_margin = (HEIGHT - grid_height * cell_size) // 2
    grid_rect = pygame.Rect(left_margin, top_margin, grid_width * cell_size, grid_height * cell_size)
    pygame.draw.rect(screen, (255, 0, 0), grid_rect)
    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x, y]:
                rect = pygame.Rect(left_margin + x * cell_size, top_margin + y * cell_size, cell_size, cell_size)
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
left_margin = (WIDTH - grid_width * cell_size) // 2
top_margin = (HEIGHT - grid_height * cell_size) // 2
grid_rect = pygame.Rect(left_margin, top_margin, grid_width * cell_size, grid_height * cell_size)

# Button properties
button_width = 150
button_height = 50
button_font = pygame.font.SysFont(None, 35)
button_color = (0, 255, 0)

# Top row button properties
top_row_button_top = HEIGHT - 133

# Bottom row button properties
bottom_row_button_top = HEIGHT - 68

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

# Grid Size button
size_button_left = (WIDTH - (100 + button_width * 3)) // 2
size_button_rect = pygame.Rect(size_button_left, bottom_row_button_top, button_width, button_height)
size_button_text = button_font.render("Grid Size", True, (0, 0, 0))

# Evolve button
evolve_button_left = size_button_left + button_width + 50
evolve_button_rect = pygame.Rect(evolve_button_left, bottom_row_button_top, button_width, button_height)
evolve_button_text = button_font.render("Evolve", True, (0, 0, 0))

# Stop button
stop_button_left = evolve_button_left + button_width + 50
stop_button_rect = pygame.Rect(stop_button_left, bottom_row_button_top, button_width, button_height)
stop_button_text = button_font.render("Stop", True, (0, 0, 0))

running = True
paused = True
clock = pygame.time.Clock()

while running:
    clock.tick(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if next_button_rect.collidepoint(event.pos):
                    paused = True
                    handle_next_button_click()
                elif populate_button_rect.collidepoint(event.pos):
                    paused = True
                    handle_populate_button_click()
                elif clear_button_rect.collidepoint(event.pos):
                    paused = True
                    handle_clear_button_click()
                elif size_button_rect.collidepoint(event.pos):
                    paused = True
                    # Get user input for grid size
                    width_input_box = pygame.Rect((WIDTH - 100) // 2, 300, 100, 50)
                    height_input_box = pygame.Rect((WIDTH - 100) // 2, 400, 100, 50)             
                    # Back button
                    back_button_left = (WIDTH - (50 + button_width * 2)) // 2
                    back_button_rect = pygame.Rect(back_button_left, 500, button_width, button_height)
                    back_button_text = button_font.render("Back", True, (0, 0, 0))
                    # Enter button
                    enter_button_left = back_button_left + button_width + 50
                    enter_button_rect = pygame.Rect(enter_button_left, 500, button_width, button_height)
                    enter_button_text = button_font.render("Enter", True, (0, 0, 0))
                    color_inactive = pygame.Color('lightskyblue3')
                    color_active = pygame.Color('dodgerblue2')
                    width_color = color_inactive
                    height_color = color_inactive
                    width_user_input = ''
                    height_user_input = ''
                    active = True

                    while active:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                running = False
                                active = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if width_input_box.collidepoint(event.pos):
                                    active = True
                                    width_color = color_active
                                    height_color = color_inactive
                                elif height_input_box.collidepoint(event.pos):
                                    active = True
                                    width_color = color_inactive
                                    height_color = color_active
                                elif back_button_rect.collidepoint(event.pos):
                                    active = False
                                    width_color = color_inactive
                                    height_color = color_inactive
                                elif enter_button_rect.collidepoint(event.pos):
                                    if active:
                                        try:
                                            new_width, new_height = int(width_user_input.strip()), int(height_user_input.strip())
                                            new_cell_size = min((DEFAULT_GRID_WIDTH * DEFAULT_CELL_SIZE) // new_width, (DEFAULT_GRID_HEIGHT * DEFAULT_CELL_SIZE) // new_height)
                                            if new_width > 0 and new_height > 0 and new_cell_size > 0:
                                                grid_width, grid_height = new_width, new_height
                                                cell_size = new_cell_size
                                                grid = np.zeros((grid_width, grid_height), dtype=bool)
                                                active = False
                                                color = color_inactive
                                                width_user_input = ''
                                                height_user_input = ''
                                                generation = 0
                                                draw_grid()
                                        except ValueError:
                                            width_user_input = ''
                                            height_user_input = ''
                                else:
                                    width_color = color_inactive
                                    height_color = color_inactive
                            elif event.type == pygame.KEYDOWN:
                                if active:
                                    if event.key == pygame.K_BACKSPACE:
                                        if width_color == color_active:
                                            width_user_input = width_user_input[:-1]
                                        elif height_color == color_active:
                                            height_user_input = height_user_input[:-1]
                                    else:
                                        if width_color == color_active:
                                            width_user_input += event.unicode
                                        elif height_color == color_active:
                                            height_user_input += event.unicode
                        screen.fill((0, 0, 0))
                        font = pygame.font.SysFont(None, 24)
                        txt_width = font.render("Width: ", True, width_color)
                        screen.blit(txt_width, ((WIDTH - 100) // 2, width_input_box.y - 20))
                        txt_height = font.render("Height: ", True, height_color)
                        screen.blit(txt_height, ((WIDTH - 100) // 2, height_input_box.y - 20))
                        input_font = pygame.font.SysFont(None, 35)
                        input_width = input_font.render(width_user_input, True, width_color)
                        screen.blit(input_width, ((WIDTH - 100) // 2 + (100 - input_width.get_width()) // 2, 300 + (50 - input_width.get_height()) // 2))
                        input_height = input_font.render(height_user_input, True, height_color)
                        screen.blit(input_height, ((WIDTH - 100) // 2 + (100 - input_height.get_width()) // 2, 400 + (50 - input_height.get_height()) // 2))
                        pygame.draw.rect(screen, width_color, width_input_box, 2)
                        pygame.draw.rect(screen, height_color, height_input_box, 2)
                        pygame.draw.rect(screen, button_color, back_button_rect)
                        screen.blit(back_button_text, (back_button_left + (button_width - back_button_text.get_width()) // 2, 500 + (button_height - back_button_text.get_height()) // 2))
                        pygame.draw.rect(screen, button_color, enter_button_rect)
                        screen.blit(enter_button_text, (enter_button_left + (button_width - enter_button_text.get_width()) // 2, 500 + (button_height - enter_button_text.get_height()) // 2))
                        pygame.display.flip()
                elif evolve_button_rect.collidepoint(event.pos):
                    paused = False
                elif stop_button_rect.collidepoint(event.pos):
                    paused = True 
                elif grid_rect.collidepoint(event.pos):
                    paused = True
                    cell_x = (event.pos[0] - left_margin) // cell_size
                    cell_y = (event.pos[1]  - top_margin) // cell_size
                    handle_cell_click(cell_x, cell_y)
        if not paused:
            grid = update_grid()

    draw_grid()

    # Generation text
    gen_text = button_font.render("Generation: " + str(generation), True, (255, 255, 255))
    screen.blit(gen_text, (100, 100))

    # Population text
    pop_text = button_font.render("Population: " + str(population), True, (255, 255, 255))
    screen.blit(pop_text, (WIDTH - 100 - pop_text.get_width(), 100))

    pygame.draw.rect(screen, button_color, populate_button_rect)
    screen.blit(populate_button_text, (populate_button_left + (button_width - populate_button_text.get_width()) // 2, top_row_button_top + (button_height - populate_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, clear_button_rect)
    screen.blit(clear_button_text, (clear_button_left + (button_width - clear_button_text.get_width()) // 2, top_row_button_top + (button_height - clear_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, next_button_rect)
    screen.blit(next_button_text, (next_button_left + (button_width - next_button_text.get_width()) // 2, top_row_button_top + (button_height - next_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, size_button_rect)
    screen.blit(size_button_text, (size_button_left + (button_width - size_button_text.get_width()) // 2, bottom_row_button_top + (button_height - size_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, evolve_button_rect)
    screen.blit(evolve_button_text, (evolve_button_left + (button_width - evolve_button_text.get_width()) // 2, bottom_row_button_top + (button_height - evolve_button_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, stop_button_rect)
    screen.blit(stop_button_text, (stop_button_left + (button_width - stop_button_text.get_width()) // 2, bottom_row_button_top + (button_height - stop_button_text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()