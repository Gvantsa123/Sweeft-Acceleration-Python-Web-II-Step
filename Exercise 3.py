def bomber_man(n, grid):
    grid = [[c for c in row] for row in grid]

    # define helper function for planting bombs
    def plant_bombs():
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '.':
                    grid[i][j] = 'O'

    # define helper function for detonating bombs
    def detonate_bombs():
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 'O':
                    # detonate the bomb
                    grid[i][j] = '.'
                    if i > 0 and grid[i-1][j] == 'O':
                        grid[i-1][j] = '.'
                    if j > 0 and grid[i][j-1] == 'O':
                        grid[i][j-1] = '.'
                    if i < len(grid)-1 and grid[i+1][j] == 'O':
                        grid[i+1][j] = '.'
                    if j < len(grid[i])-1 and grid[i][j+1] == 'O':
                        grid[i][j+1] = '.'

    # initialize grid
    t = 0
    while t < n:
        t += 1
        if t % 2 == 0:
            plant_bombs()
        else:
            detonate_bombs()
            if t % 4 == 3:
                plant_bombs()

    return [''.join(row) for row in grid]

# read input from user
n = int(input().strip())
grid = []
for i in range(6):
    row = input().strip()
    grid.append(row)

# call bomber_man function and print output
output = bomber_man(n, grid)
for row in output:
    print(row)