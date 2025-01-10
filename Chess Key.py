from typing import List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Piece:
    type: str
    col: int
    row: int


def parse_position(pos: str) -> Piece:
    piece_type = pos[0]
    col = ord(pos[1]) - ord("A")
    row = 8 - int(pos[2])
    return Piece(piece_type, col, row)


def get_valid_moves(piece: Piece, board: List[Piece]) -> Set[Tuple[int, int]]:
    moves = set()

    def is_occupied(col: int, row: int) -> bool:
        return any(p.col == col and p.row == row for p in board)

    def add_if_valid(col: int, row: int):
        if 0 <= col < 8 and 0 <= row < 8 and not is_occupied(col, row):
            moves.add((col, row))

    if piece.type in ["Q", "R"]:
        for col in range(8):
            add_if_valid(col, piece.row)
        for row in range(8):
            add_if_valid(piece.col, row)

    if piece.type in ["Q", "B"]:
        for i in range(-7, 8):
            add_if_valid(piece.col + i, piece.row + i)
            add_if_valid(piece.col + i, piece.row - i)

    moves.discard((piece.col, piece.row))
    return moves


def count_positions(pieces: List[Piece], depth: int, last_moved_idx: int = -1) -> int:
    if depth == 0:
        return 1

    total = 0
    seen_positions = set()

    for i, piece in enumerate(pieces):
        if i == last_moved_idx:
            continue  # Skip piece that moved in previous ply

        valid_moves = get_valid_moves(piece, pieces)
        for new_col, new_row in valid_moves:
            # Create new board state
            new_pieces = pieces.copy()
            new_pieces[i] = Piece(piece.type, new_col, new_row)

            # Create unique position signature
            pos_key = tuple(sorted((p.type, p.col, p.row) for p in new_pieces))

            if pos_key not in seen_positions:
                seen_positions.add(pos_key)
                if depth == 1:
                    total += 1
                else:
                    total += count_positions(new_pieces, depth - 1, i)

    return total


def solve(input_str: str) -> int:
    lines = input_str.strip().split("\n")
    pieces = [parse_position(pos) for pos in lines[0].split()]
    depth = int(lines[1])

    if not (0 < depth < 5):
        return 0

    return count_positions(pieces, depth)


# Test cases
test_cases = ["QA3 RB3\n1", "QA3\n2", "QA3 RB3\n2"]

for i, test in enumerate(test_cases, 1):
    result = solve(test)
    print(f"Test {i}: {result}")
