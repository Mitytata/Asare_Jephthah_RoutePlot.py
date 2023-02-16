def create_blank_grid(size: int = 12) :

    """
    Create blank grid.
    Parameters
    ----------
    size: int
        Size of grid.
    Returns
    -------
    list
        Empty grid.
    """

    return [['   ' for _ in range(size)] for _ in range(size)]

def get_grid_number(i: int) :

    """
    Get the grid number.
    Parameters
    ----------
    i: int
        Index number.
    Returns
    -------
    str
        Grid number.
    """   

    return f" {str(i+1).zfill(2)}"

def print_grid(grid: list) :

    """
    Print the grid.
    Parameters
    ----------
    grid: list
        Grid to be printed.
    Returns
    -------
    None
    """    

    row_num = len(grid)
    grid_text = '\n'

    for row in reversed(grid):
        grid_text += get_grid_number(row_num)
        for square in row:
            grid_text += square
        grid_text += '\n'
        row_num -= 1

    grid_text += '  '
    for i, _ in enumerate(grid[0]):
        grid_text += get_grid_number(i)
    
    print(grid_text + '\n')

def populate_grid_and_get_coordinates(start_x: int, start_y: int, bearings: list):
    
    """
    Populate the grid and get the coordinates.
    Parameters
    ----------
    start_x: int
        Starting x co-ordinate.
    start_y: int
        Starting y co-ordinate.
    bearings: list
        Bearings.
    Returns
    -------
    None
    """

    coordinates = [(start_x, start_y)]

    grid = create_blank_grid()
    grid[start_y-1][start_x-1] = ' START '

    direction_indicators = {
        'N': 'x',
        'E': 'x',
        'S': 'x',
        'W': 'x'
    }

    direction_indicator = direction_indicators[bearings[1]]

    print(f"Starting position: ({start_x}, {start_y})")
    print(f"Direction indicator: {direction_indicator}")

    for bearing in bearings:
        if bearing == 'N':
            start_y += 1
        elif bearing == 'S':
            start_y -= 1
        elif bearing == 'E':
            start_x += 1
        elif bearing == 'W':
            start_x -= 1
        else:
            print_grid(grid)
            print(coordinates)
            print("\n")
            return

        if start_x < 1 or start_y < 1 or start_x > len(grid) or start_y > len(grid):
            print(f'\n* ERROR: Outside of the grid. Drone path leaves grid attempting to go {bearing} from {start_x},{start_y}')
            print('\nKey: S = Start')
            print('     E = Drone path leaves grid')

            grid[start_y-1][start_x-1] = ' E '
            coordinates.append(('ERROR'))
            print_grid(grid)
            print(coordinates)
            return

        if bearing in direction_indicators:
            grid[start_y-1][start_x-1] = f' {direction_indicators[bearing]} '
        else:
            print_grid(grid)
            print(coordinates)
            return

        coordinates.append((start_x, start_y))

    grid[start_y-1][start_x-1] = ' F '
    
    print('\nKey: S = Start')
    print('     F = Finish')
    print_grid(grid)
    print(coordinates)


while True:
    prompt_text = "Enter the next route instructions file or enter STOP to finish: "
    instruction = input(prompt_text)
    
    if instruction.lower() == 'STOP':
        print('Program Ended')
        break
    
    try:
        f = open(instruction, 'r')
    except FileNotFoundError as e:
        print(e)
        print(f'* {instruction} was not found.\n')
        continue

    lines = f.read().split('\n')
    
    try: 
        x,y = int(lines[0]), int(lines[1])      
    except ValueError as e: 
        print(e)
        print(f'* The first two lines of file {instruction} should each contain one integer')
        print(f'    Please review {instruction} and correct!')
        continue
    
    populate_grid_and_get_coordinates(x, y, lines[2:])