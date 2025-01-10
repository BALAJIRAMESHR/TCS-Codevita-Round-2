def get_coordinates(curr_pos, move):
    ly, y, x = curr_pos
    if move == "u":
        return (ly, y - 1, x)
    elif move == "d":
        return (ly, y + 1, x)
    elif move == "f":
        return (ly + 1, y, x)
    elif move == "b":
        return (ly - 1, y, x)
    elif move == "r":
        return (ly, y, x + 1)
    elif move == "l":
        return (ly, y, x - 1)
    return curr_pos


def is_valid_position(pos, S):
    """Check if all coordinates are within bounds."""
    return all(0 <= coord < S for coord in pos)


def get_band_positions(start_pos, sequence, S):
    """Generate all positions for a band's movement."""
    positions = []
    curr_pos = start_pos
    positions.append(curr_pos)

    for move in sequence:
        next_pos = get_coordinates(curr_pos, move)
        if not is_valid_position(next_pos, S):
            return None
        positions.append(next_pos)
        curr_pos = next_pos

    return positions


def are_bands_interlocked(band1_positions, band2_positions):
    """Check if the two bands are interlocked."""
    band1_set = set(band1_positions)
    band2_set = set(band2_positions)

    # Check for direct overlaps
    if band1_set & band2_set:
        return True

    # Check for 3D interlocking segments
    for i in range(len(band1_positions) - 1):
        pos1, next1 = band1_positions[i], band1_positions[i + 1]
        for j in range(len(band2_positions) - 1):
            pos2, next2 = band2_positions[j], band2_positions[j + 1]

            # Check if segments cross in 3D space
            if (
                pos1[1:] == pos2[1:]
                and next1[1:] == next2[1:]
                and (
                    (pos1[0] < pos2[0] and next1[0] > next2[0])
                    or (pos1[0] > pos2[0] and next1[0] < next2[0])
                )
            ):
                return True

    return False


def count_overlaps(band1_positions, band2_positions):
    """Count the overlaps where one band is above another."""
    overlap_count = 0
    for pos1 in band1_positions:
        for pos2 in band2_positions:
            if pos1[1:] == pos2[1:]:  # Same (y, x) position
                if pos1[0] > pos2[0]:  # band1 is above band2
                    overlap_count += 1
    return overlap_count


def solve_friendship_bands(S, start1, seq1, start2, seq2):
    """Determine whether the bands interlock or the max overlap count."""
    band1_positions = get_band_positions(start1, seq1, S)
    band2_positions = get_band_positions(start2, seq2, S)

    # Check for invalid positions
    if band1_positions is None or band2_positions is None:
        return "Impossible"

    # Check for interlocking
    if are_bands_interlocked(band1_positions, band2_positions):
        return "Impossible"

    # Count overlaps
    overlaps_1_above_2 = count_overlaps(band1_positions, band2_positions)
    overlaps_2_above_1 = count_overlaps(band2_positions, band1_positions)

    return str(max(overlaps_1_above_2, overlaps_2_above_1))


if __name__ == "__main__":
    try:
        S = int(input().strip())
        start1 = tuple(map(int, input().strip().split()))
        seq1 = input().strip()
        start2 = tuple(map(int, input().strip().split()))
        seq2 = input().strip()

        result = solve_friendship_bands(S, start1, seq1, start2, seq2)
        print(result)
    except Exception:
        print("Impossible")
