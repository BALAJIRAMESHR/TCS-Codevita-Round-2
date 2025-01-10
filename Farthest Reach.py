from collections import deque
from typing import List, Tuple


def is_valid(x: int, y: int, n: int, m: int) -> bool:
    """Check if coordinates are within grid bounds."""
    return 0 <= x < n and 0 <= y < m


def is_stable(grid: List[str], x: int, y: int, n: int) -> bool:
    """Check if a cell is stable (has building below or is in last row)."""
    if x == n - 1:  # Last row
        return True
    return x + 1 < n and grid[x + 1][y] == "B"


def get_valid_moves(
    x: int, y: int, grid: List[str], n: int, m: int
) -> List[Tuple[int, int]]:
    """Get valid adjacent moves (no diagonals)."""
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    valid_moves = []

    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if is_valid(new_x, new_y, n, m) and grid[new_x][new_y] != "B":
            valid_moves.append((new_x, new_y))

    return valid_moves


def apply_gravity(grid: List[str], x: int, y: int, n: int) -> Tuple[int, int, int]:
    """Apply gravity until reaching a stable position."""
    original_x = x
    while x < n - 1 and not is_stable(grid, x, y, n):
        x += 1
        if x < n and grid[x][y] == "B":  # Can't land on building
            x -= 1
            break
    return x, y, x - original_x  # Return gravity cost


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)


def find_farthest_reach(
    n: int, m: int, grid: List[str], k: int
) -> List[Tuple[int, int]]:
    """Find all cells with maximum Manhattan distance reachable within k steps."""
    # Find starting position
    start_x = start_y = -1
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                start_x, start_y = i, j
                break
        if start_x != -1:
            break

    # Apply gravity to starting position
    start_x, start_y, _ = apply_gravity(grid, start_x, start_y, n)

    # BFS with steps tracking
    visited = {}  # (x, y) -> min steps to reach
    queue = deque([(start_x, start_y, 0)])  # (x, y, steps)
    max_distance = -1
    result_cells = []

    while queue:
        x, y, steps = queue.popleft()

        if steps > k:
            continue

        if (x, y) in visited and visited[(x, y)] <= steps:
            continue

        visited[(x, y)] = steps

        # If current cell is stable, consider it
        if is_stable(grid, x, y, n) and grid[x][y] != "B":
            dist = manhattan_distance(start_x, start_y, x, y)
            if dist > max_distance:
                max_distance = dist
                result_cells = [(x, y)]
            elif dist == max_distance:
                result_cells.append((x, y))

        # Try each valid move
        for next_x, next_y in get_valid_moves(x, y, grid, n, m):
            # Apply gravity after move
            final_x, final_y, gravity_cost = apply_gravity(grid, next_x, next_y, n)
            total_steps = steps + 1 + gravity_cost  # Move + gravity

            if total_steps <= k:
                queue.append((final_x, final_y, total_steps))

    # Sort by row then column
    return sorted(result_cells)


def main():
    # Read input
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    k = int(input())

    # Find solution
    result = find_farthest_reach(n, m, grid, k)

    # Print output - one coordinate pair per line, with space between coordinates
    for x, y in result:
        print(f"{x} {y}")


if __name__ == "__main__":
    main()
