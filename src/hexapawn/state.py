"""
State representation (RL component: State).

The state is the full information needed to make a decision:
- Board configuration (who is on each cell).
- Whose turn it is.

We use a hashable representation so it can be used as a key in the Q-table.
"""

# Board is 3x3. Cell values: 0 = empty, 1 = white, -1 = black.
# We store board as a tuple of 9 integers (row-major).
BoardTuple = tuple[int, int, int, int, int, int, int, int, int]

# Turn: 1 = white to move, -1 = black to move.
# State = (board, turn) — hashable for tabular Q-learning.
State = tuple[BoardTuple, int]

ROWS = 3
COLS = 3
WHITE = 1
BLACK = -1
EMPTY = 0


def cell_index(row: int, col: int) -> int:
    """Linear index for (row, col) in row-major order."""
    return row * COLS + col


def index_to_pos(i: int) -> tuple[int, int]:
    """(row, col) from linear index."""
    return i // COLS, i % COLS


def initial_state() -> State:
    """Initial Hexapawn: white on row 0, black on row 2, white to move."""
    board: BoardTuple = (
        WHITE, WHITE, WHITE,
        EMPTY, EMPTY, EMPTY,
        BLACK, BLACK, BLACK,
    )
    return (board, WHITE)


def get_cell(board: BoardTuple, row: int, col: int) -> int:
    """Return piece at (row, col): 0, 1, or -1."""
    if not (0 <= row < ROWS and 0 <= col < COLS):
        raise IndexError(f"({row}, {col}) out of bounds")
    return board[cell_index(row, col)]


def set_cell(board: BoardTuple, row: int, col: int, value: int) -> BoardTuple:
    """Return a new board with (row, col) set to value."""
    i = cell_index(row, col)
    return board[:i] + (value,) + board[i + 1:]


def state_to_string(state: State) -> str:
    """Human-readable board for debugging (white = W, black = B)."""
    board, turn = state
    chars = {EMPTY: ".", WHITE: "W", BLACK: "B"}
    lines = []
    for r in range(ROWS):
        line = " ".join(chars[get_cell(board, r, c)] for c in range(COLS))
        lines.append(line)
    lines.append(f"Turn: {'White' if turn == WHITE else 'Black'}")
    return "\n".join(lines)
