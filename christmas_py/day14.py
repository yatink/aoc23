import copy


def tilt_column(column: list[str]) -> list[str]:
    stopping_pt = -1
    curr = 0
    while curr < len(column):
        # If it's a rolling stone
        if column[curr] == 'O':
            # Move it
            column[curr] = '.'
            column[stopping_pt + 1] = 'O'
            # Update stopping pt
            stopping_pt += 1
        elif column[curr] == '#':
            # Only update stopping pt
            stopping_pt = curr
        curr += 1
    return column


def process_column(column: list[str]) -> int:
    updated = tilt_column(column)
    rocks = [idx for (idx, x) in enumerate(reversed(updated), start=1) if x == 'O']
    return sum(rocks)


def tilt_up(grid: list[list[str]]) -> None:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for c in range(num_cols):
        col = [grid[r][c] for r in range(num_rows)]
        new_col = tilt_column(col)
        for idx, elem in enumerate(new_col):
            grid[idx][c] = elem
    

def tilt_down(grid: list[list[str]]) -> None:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for c in range(num_cols):
        col = [grid[r][c] for r in range(num_rows)]
        new_col = tilt_column(list(reversed(col)))
        for idx, elem in enumerate(reversed(new_col)):
            grid[idx][c] = elem



def tilt_left(grid: list[list[str]]) -> None:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for r in range(num_rows):
        row = grid[r]
        new_row = tilt_column(row)
        grid[r] = new_row


def tilt_right(grid: list[list[str]]) -> None:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for r in range(num_rows):
        row = grid[r]
        new_row = tilt_column(list(reversed(row)))
        grid[r] = list(reversed(new_row))


def parse_input(inpt: str) -> list[list[str]]:
    return [list(l) for l in inpt.split("\n")]


def stringify(grid: list[list[str]]) -> str:
    return "".join(["".join(l) for l in grid])


def calculate_load(grid: list[list[str]]) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])
    columns = [[grid[r][c] for r in range(num_rows)] for c in range(num_cols)]
    s = 0
    for c in columns:
        rocks = [idx for (idx, x) in enumerate(reversed(c), start=1) if x == 'O']
        s += sum(rocks)
    return s


def part2(inpt: str) -> int:
    grid = parse_input(inpt)
    num_rows = len(grid)
    num_cols = len(grid[0])
    ct = 0
    sums = []
    cache: dict[str, tuple[int, int]] = {}
    cache2: dict[int, tuple[list[list[str]],int]] = {}
    cache[stringify(grid)] = (calculate_load(grid), 0)
    cache2[0] = (grid, calculate_load(grid))
    while ct < 100000000:
        ct += 1
        tilt_up(grid)
        tilt_left(grid)
        tilt_down(grid)
        tilt_right(grid)
        grid_str = stringify(grid)
        if grid_str in cache:
            # Found a cycle
            break
        else:
            cache[grid_str] = (calculate_load(grid), ct)
            cache2[ct] = (grid, calculate_load(grid))

    _, initial_offset = cache[grid_str]
    cycle_length = ct - initial_offset
    equivalent_idx = ((1000000000 - initial_offset) % cycle_length) + initial_offset
    return cache2[equivalent_idx][1]
        

def part1(inpt: str) -> int:
    lines = inpt.split('\n')
    num_rows = len(lines)
    num_cols = len(lines[0])
    columns = [[lines[r][c] for r in range(num_rows)] for c in range(num_cols)]
    return sum(process_column(c) for c in columns)


if __name__ == '__main__':
    test_inpt = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    real_inpt = """O#O#O#O..OO....#O..........#.#OO..........#..#....O.........O#...#...OOO.O.#.##...#.#..##..O.....#..
#.#....O..O...#..O...O.##.OO....#.#.O..#.OOO.O....#..#..OO......O#...#.#.#O.O..#OO..O.....#.##O...O.
###O#O#O.O#..OOOO.........#.#.O#.OO..#.##.#..O....O....#.O.#..O..O####.#..O#...O....OO..#O.....OO..#
.##.O#.......#....O#.......O.......OO......#...OO#..#####.O.......OOOO###O............#O..#O#.....O.
....O..#.#.#...O......O........O#..O..#O.#O...#O.#O...O#.#...#.O....##.OO.#...........#O.#O#...O....
O...O..O.....#..O.#...O.OO..##..#OO...O........O.O.......O.#O.#..O......O#.......#O.....O.#....#..O#
.....O.OO..OO.....O##.....O.#........##.O.#..O..#OO...#.#..#....#O..#.OO...OO#...#..O.....#OO..#.O..
#..#OOO.O.....OO...O##..........###..##.O#...O.O...#..O#...........OO..#O..#..O#O......O#.#....#.O#O
..#O...#.#OOO..#O.O..#O..#....O......O.O...O##O.....................O..##....#...O...#..#......#....
.#...#.#.#O.O...#.O.#.#O.......#.....O.#.....OO....O.OO.#OO.#...OO..O.O#.OO.O...##...O..#...O#..O.O.
....OO#...###...##O...O.#..OO#..#.......O#....#.#.#..O..O..O......O.....OO#O..#...#....#.#O..#O.....
.OO....O..........O..##.OO#O.....O#.O..O.O...........##O..O......OO.O...O#.#.#.#O...##....#O..O..O.#
...O#.....O....#.........OO........O#.#O....O......O....#..#.##.#.#O##.#......#...OO.#....O.......#.
..#.O...#..#...O...#.#.........OO.........O#......###.#.#.O.O..O..O.#O...O#O.#....O..O...O.#......O.
..#.............#OO.....##...#O....O...#...O....#O..#O...#.#.O..O#.#.....#O#.#O#....#...O...#..###..
#..O.OO...O.......O..O.O..#...O.....O..#.O##....O#.#......#..###.......O.O..#O....O##.O......###...O
....O..O#OO.O#......OO...O#.O...##...O.###.#O.O.O..#.#O...O....OOO.O...O...#....OO.O.##.....O#O##...
#...#OO......O............#.O..#O..OO.O#.O.O...O.....O..O.OOO..O...#......O............O.#..####O...
#..#....O....O..#O.......#.OO#......##....O...#....O#...#O....#...#....O...O....O#O...O.#.O........#
...O........O#....O.#O......#.##....O#.#.O...##O.##..#.....#....OO..OO.....#.#.#####......#.O.......
.#O......#..#O#..O.##.....#.......OO###....O#..O##.O#OO.#.#.OO##.OO.#....#.#.#.....OO....#O#...O....
OO..O.#OO....#...#....#..O.OO....O...O#.....O...#.O.O....O.O...O###....O.O..O.#.O.........O#....O#O#
.O..OO..##.O.#OO.OOO#........#.OO#....O..#O...O#.#....O.O.##O..O.O...O#...........O...O.##O.##....O#
....#...O.#.....O#..#.#...O.OOO.#.....O..O.#O...#O....O.O#.O#.O....#O#......##......O.#.....O...OO#.
..#..O.....O.....#..O...O...#.....O.O.O...OO.O####..O#.##..O#...#..O#..O...O.###..#......O.O.....#..
..O..O#.......OO.#.O.O#.#O..OO..O..#O....#......O.......OO#...#.#.......OOO##....O....O.....#O#..#.O
O#..O.O.......O#.OO....O...#OOO.#O#O.O#....O####.#......#.......O....#O#..#.#.....O..O.#.#O..#.O..OO
#..#.#.O.O..O...O.........O.#.O...OO.....#..#...#...O..OO.O..#...#..O.O.O....O#..O....#O#..O#.O.##..
#.......##..O.O..###O.OO....#OO.#O..O..#.O..####O#.O......O...O#........#.#.O.O.#...##.OO..##...#O..
OOOO#O...##...#.......O....O..OO.O##..O#.O.......O#....O##.O.....O#....O..O.....#.......O#....OO#...
O..#.O#.#.OO..OO.OO..OO..O#...O#.O.....O........O.......#..#..#..O.OO.........O.O.....O.OO...O..O.#.
....OOO......OOO..#....#.O..O#...O....##...O...O##O..#O.#.OO.O.....OO.O#.#...OO..O...##......#..O.#O
.#....#.O.#...O.O.O#...OO..O.#.............OO.#..........O....#..OO#.#.O....OO.OO##.O...##....OO..O.
...OO...O#O#O......##..O.OOO..O.#..O..O#.O#O....#..##..#....O.#.O..OO.O.....#O.O..#.O..#...#.O.#....
O....O.O.....O.O....#.#..O.OOO.O..#....OO.O..O#OO..O#..#.O.O......O.O..O#O..O.#.#...O...O..###.O....
........#.O.O#O#O..#...#.O.O..#.OO.#...O.......O....O.O#....O....O.O..O#..O#....O.....#.O....#O.O.O#
...##.O##..O.......O.OO..#O......O...............#.OO.....OO#....#..OO..O...O..#OO..O..O..##....OO#O
.##.#.#O.......O..O...O...OO...O#....##.#OO..O.....#OO.#.OO.....O..#.O.#......O.O.#.O...#....#.O#...
...O.####.#O#..O..OO.O..OOO#.#O..#O.O#.#O..#.#...#O....#...#.#.#....##..##.......#.O..#OOO...O.#....
..#O..O#O.OO.O.O....O.O...O#....##..##OO.#...#...O.OO#...O..#....O#.....#.O#OO..O........O....O...#.
....#OO.O.#.#.#O.......O..O#........#.#OO.####..O#........#.O#....#..O..O#..#.O.OO.O.......#.O..O..#
.#.#..OO#.#...#.OO...#...O#...##.#......#OO....#...OOOOO#..#O.#.#..#O.....#..OO.#.#....O...O.O......
O#..#OO......#.O.#..O.......OO...O.O...OO..##....#...#.#OOO......#.#.O.O..###O.OO.O...#.O....O...#..
O...O.O..OO..#O#.O.#.O..#..O#..#...#..O.O.........O#..##.....#.O...#O.....O.#.#O.OO.O.#O.O#...O.O#OO
......O..#.....#.O#...O..OO..O....#..O.....#.#OO....O.O.O.#..#.......O...O.O...O.O.O.O.##..##.OO.O..
.....OO##.....O..O#O.#.O.O...#......#.#....OO..OOO#..##.#O..O.#.#OOO.#O...O......OO.##..O.#.O.......
#.....O.......#......O..#..O.#.##...O.O..O........OO...O#O.###...O.#.O.O........#.#O...O##OO#.....##
O.O..#....O....#.O.O#O.O.....O..##....##...O...#O...#.#...O..#..O.......#..#.......##..O...O...O.OO.
.#.#.O.....O##O...###....O.O......#O...OO......O###O.O.......#..............O.O.O#.O......#...O#....
##O....O.......#..O...........O...#...#.O......#..O#.OO..#...#...O.....#......O.O........O#.O#.OO...
O#....O.......O.OO.#..O.........##....OO....#O.#...OOO#......O.......OOO#O.O.O#.#..#..#OO..OO..O...O
.O..#.O....OO.#O....#O......#...#O..O#.O#OO#.......O.#.....#......O....O...#..O#.....#...##..#.#.#.#
.....OO#....#......O.....OO.O#O#.........#.#......O.##....O.OO....##.#O..OO...O#.#....O..OO.O..#.O..
.....#...#....OO......O...#....#OO#.##.O.OO#O.O..O.O.......O...#..O...OO....OOO......O#.....#.O.....
.##..OO##......OOO....O.#.#...O#.O...O...#....O#..#...O.....O...#.....#O....O...OO#.O.OO...O..##...O
O..#OO#O#.##.#....OO.O.....O..#..O..#.#O...#.#.O...#O...O.....O.O....OO........#.#.OO.OO....OOO.#...
O...OO.O..##O..O.....O#...O.....O..#.....#.O..#...#.O.##.O##....O.O.....O#.#.O.O..#..O.....O........
O..O#.O....O#.O#.O.O.O...#O.....#....O..O.OO#O...#.#O#........#..OO#O..#..O.#O.....O...O....#O.#....
...#O.#..#O..O#O........O..O#........O#....##......OO#.#..O.#OO..##..O..........#.......#O....O#.O.#
.O..OO...###.O........O..........O..#.##.##.##.#O...O.##...O..##.##...O###.....#..#.O#O.OOO.OOO#...O
........##.O..#O#.....#..#...O..#.O......#OOOO##......#.O.O.....#.##......OO.#...#.O....O..O.OOO.#..
#.#....#.............OO....OO#.OO#..........OO.OO.O.O.O.....O.....O....#....#.#.#...O...#..##.......
..#O#OO...#.....#.......##O..#O......O.....O.O.O...#.....#O.O...O....#.O...#O.O.#....O...#.##.O.....
.....#...#.#..O.O.O.#....O##O.....O...#O.O....#.....##.O....O...#...O.#.....##....#.O...#......OO#..
O..#......OO#.....OO#..OOO..O.OO.....O.....#....O...O....##.O#.....##.O#.#OO...#.#.......#...#......
.O......O#.....O.O........##.O.O...#.OO...#OO..O#OOOO.....#........#..#.#..O#..#....O.#...#.....##O#
#.O...O#.#.#....##..O..........#.O.OO.#..#.O#....................O.OO.O#.#O..#..O#..#..OO.#O..OO##.O
O#O..O.#..#O...O....#....O##..O.O..#OO.O..O#O...O.OO.....#..O....#.....#..#...#.........O....O.O.#..
..O..O...OO......##OO#....O...#.#.....O...........O...O.#.O.#.OO#...#...OO..O.#.O.#O...#O..OO#.O...O
O..O.#O......O.O....OO..#..#...O...O#...O.OO.....O#...O..O#..O..O..#OO.#..O#....#...##O#.........#.#
O..OO#...#.OO............#OOO....O.O...#........#..#....O........OO#O....#.......##O.O.O#.#..O#O.#.#
#....O.O##..O...#..O#..#.....O.#..O.#..O#.##....O....O......#...#..OO.O..O.#OO...........#OO...#OO..
#.#.#.O.#.O.##.O....O#.#..O#...O....##O.#.O.O...#..O..O..##.O#.......##O..#O#.#.#.....O##O...O.O....
....#.....O.O.#....#..O.........O...O.O.....O#.....#...#..O.#.....OOO..#........O#.#O.....#....O#O..
......#O##.....#O##.....OO..O.O....#.O.......O.OO....#...#.O#OO..#O..O...#........##...#.....#...O..
#O..O.O...#.O##OO#..OO..O..#.#..##.O.....OO.#....O..O#..OO.......#.......OO.#.........O..........OO.
O.......O...#O.......O...#O#.O..#...#.O.......#...#.#..#O.O..........OO##.O.O..#......O...O..O#O..#.
.#......O.#......O#O...O.O....#..#O.O..#.#....O.##O#..O....O..OOO..O....OO......OO..O#O...#....#..#.
.........###.O..O........#...#..OO#.#.....#.#....#.#....#OO.O...O..O...O...O#.......O.........OO.#.#
O#O#.#.#..O..........#O..O.#.O.O##...OO......OO.O#..#O#...O.O...O..##..#.OO##..O....OO..#.OO........
O..O.O#..O#.O......O.O..OO...O.......O......#.O.OO#..###OO...##...#O.OO...OO..##..#O..OO.O....O....#
O....O..O....O..OO..##..OO...O##O...O..#O..O..O#.#O....O.....##..#O...O#.#O##.#.##O...##.#O...O.....
........O.OO#OO.###OO....O....#....O..#....#....#...O..#......O#O#O##.#O#.......O#..#O.....OOO...O..
O.....O.O..O......O.O....O.....O.....................O#..#...O.#...O.O...#..OO###...#...O##.#O......
..#O#.#O##...O..O....O#.##..OO#.O.#.OO..O#.O..##O..#OO.O.#.O##.#OO..#...O#O.O..O..O.O...#..#....O#..
...O.....O......#.O.O...O.#...O..#.OO..O...O..#..#.#...#O.....O...##O..#.....#O.#....O..O..O..O#....
..............OO#.........#.#.O...##...OO.OO..O..O##.#..O..O....O..#...#OO.OOO....#OO..O.#.#O.O.O#..
..#..O.O.O..##O.##.OO...O..##...O.O..O#.#.#..OO..OO..O#O.#O.#.....#O...OO#..O#......#..O......OO..O.
..OOO.O.#...#.O......#..OOO.#.#...O.O.O.O..#....O..O..#....#...O............O.....O..#O...O.O.O...#.
O..O.O..O.O....###OO.#..#.O.O....#.....OO.O#.O#.#.O..OO#O..#.....#.OO..O##..OO.....#...O.#.....#....
..O.O........O..OO#...##....O..O....O.......O....#....O##.......O.#.#......#..O.....O.#.#.....O...#.
.#.O#.O#..#....O.....#.O#.....OOOO..#.O...#.#....#O...O..O...#.#.....#OO#.#.#..#.O.#O...O...O.O#..O.
.O.......OO.O...#.O.OO.O.O..........#.O#........O.#.#.O...O.#O.O....OO...#......#...###OO#.#.O.O#...
..O.......#..O...#..O..##...........#.#..#....#.....#O...O.#.##.O....O#...#..O..##..O............#..
...O....#.#.#..###..O...#O.O#.O.OO...O....O#O#OO..#O..O..#...##.O...OOO.##..O..#......O..O...O.#..#.
#.#O.OO.O.#..O..O.##O.....#O..OO.....O....#.#OO...O.O..O..#O.#OO...#....#..##.........O...#.O......O
....#O.#..O.#......O..OO.#......O.O.O.OO.OO.#OO...O..#OO.O#...#O#...O.#O..O...OO.O.#O..O.O..O......O
O..O..O##....O......#O....O.O....##.OO...O.O#...O.....#O.O....OO......#.O.....#...OO.#...#...#..#.#.
....OO#.O...O.O#..OO..#.....O...O.OO..O.#...O..O..O#.....#.O#...O...#OOOO.##.#..OO...#..........#O..
..O.O.O.O.#...O..#.#OOO.#.#.##.#..O......OO.#O..O.#....#O#.O##......#.##.OO#.O.O.#..O..#O.#..#.OOO#."""
    
    print(part1(test_inpt))
    print(part1(real_inpt))
    print(part2(test_inpt))
    print(part2(real_inpt))
