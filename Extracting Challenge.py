def is_inside(x, y, lines):
    """Check if a point is inside any shape using ray casting"""
    inside = False
    for i in range(len(lines)):
        x1, y1, x2, y2 = lines[i]
        if x1 == x2:  # Vertical line
            if x1 > x and min(y1, y2) <= y <= max(y1, y2):
                inside = not inside
    return inside


def is_on_line(x, y, lines):
    """Check if a point lies on any line"""
    for x1, y1, x2, y2 in lines:
        if x1 == x2:  # Vertical line
            if x == x1 and min(y1, y2) <= y <= max(y1, y2):
                return True
        else:  # Horizontal line
            if y == y1 and min(x1, x2) <= x <= max(x1, x2):
                return True
    return False


def get_area(x, y, S, lines, R, C):
    """Calculate area covered by placing block at (x,y)"""
    if x < 0 or y < 0 or x + S > C or y + S > R:
        return 0

    area = 0
    for i in range(y, min(y + S, R)):
        for j in range(x, min(x + S, C)):
            if is_on_line(j, i, lines) or is_inside(j, i, lines):
                area += 1
    return area


def get_next_position(covered, S, lines, R, C):
    """Find next optimal position for block placement"""
    max_area = 0
    best_pos = None

    # Try all possible positions
    for y in range(R - S + 1):
        for x in range(C - S + 1):
            # Skip if position overlaps with previous placements
            if any(px <= x < px + S and py <= y < py + S for px, py in covered):
                continue

            area = get_area(x, y, S, lines, R, C)

            # Update best position based on area and tiebreaker rules
            if area > max_area:
                max_area = area
                best_pos = (x, y)
            elif area == max_area and area > 0:
                # For equal area, prefer lower position (closer to bottom)
                if (
                    best_pos is None
                    or y < best_pos[1]
                    or (y == best_pos[1] and x < best_pos[0])
                ):
                    best_pos = (x, y)

    return best_pos, max_area


def solve_extraction(C, R, S, lines):
    """Main solving function"""
    covered = set()
    total_area = 0
    turns = 0

    while True:
        pos, area = get_next_position(covered, S, lines, R, C)
        if pos is None or area == 0:
            break

        covered.add(pos)
        total_area += area
        turns += 1

    return turns, total_area


def main():
    # Read input
    C, R = map(int, input().split())
    S = int(input())
    N = int(input())
    lines = []
    for _ in range(N):
        x1, y1, x2, y2 = map(int, input().split())
        lines.append((x1, y1, x2, y2))

    # Get solution
    turns, area = solve_extraction(C, R, S, lines)

    # Print result with exact format
    print(str(turns) + "" + str(area))


if __name__ == "__main__":
    main()
