def is_grid_size_valid(rows, cols):
    return rows != 0 and cols != 0

def is_row_input_valid(row_input, cols):
    return len(row_input) == cols and all([cell in [0, 1] for cell in row_input])

def print_grid(grid):
    for row in grid:
        print("".join([str(cell) for cell in row]))
    print("")

def get_next_gen(grid, n, m):
    updated_grid = [[0 for j in range(m)] for i in range(n)]

    for i in range(n):
        for j in range(m):
            neighbours_pos = [((i - 1) % n, j), ((i - 1) % n, (j + 1) % m), (i, (j + 1) % m), ((i + 1) % n, (j + 1) % m), ((i + 1) % n, j), ((i + 1) % n, (j - 1) % m), (i, (j - 1) % m), ((i - 1) % n, (j - 1) % m)]
            neighbours = [grid[pos[0]][pos[1]] for pos in neighbours_pos]
            live_neighbours = sum(neighbours)
            if grid[i][j] and live_neighbours in [2, 3]:
                updated_grid[i][j] = 1
            elif not grid[i][j] and live_neighbours == 3:
                updated_grid[i][j] = 1
            else:
                updated_grid[i][j] = 0

    return updated_grid

def print_generations(grid, rows, cols, gens):
    for i in range(gens):
        grid = get_next_gen(grid, rows, cols)
        print("Gen " + str(i + 1) + ": ")
        print_grid(grid)

def driver():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    if not is_grid_size_valid(rows, cols):
        raise ValueError("Invalid grid size.")
    
    grid = []
    for row in range(rows):
        row_i = input("Enter the space-separated cells of row " + str(row + 1) + ": ")
        row_i = list(map(lambda x: int(x), row_i.split()))
        if not is_row_input_valid(row_i, cols):
            raise ValueError("Invalid input for the grid.")
        grid.append(row_i)

    print("Initial grid: ")
    print_grid(grid)

    gens = int(input("Enter the number of generations: "))
    print_generations(grid, rows, cols, gens)

if __name__ == "__main__":  
    try:
        driver()
    except Exception as e:
        print(str(e))