"""
Action space (RL component: Actions).

From a given state we define the set of legal actions.
Each action is a move: (from_row, from_col, to_row, to_col).
We return a list of legal actions so the agent can index into them.
"""

from .state import (
    ROWS,
    COLS,
    WHITE,
    BLACK,
    EMPTY,
    State,
    get_cell,
)

# Action = (from_row, from_col, to_row, to_col)
Action = tuple[int, int, int, int]


def legal_actions(state: State) -> list[Action]:
    """
    Return all legal moves for the current player in this state.
    Pawns move forward one square (if empty) or capture diagonally forward.
    """
    board, turn = state
    moves: list[Action] = []

    if turn == WHITE:
        # White moves "down" (row increases).
        dr = 1
        my_piece = WHITE
        opp_piece = BLACK
    else:
        # Black moves "up" (row decreases).
        dr = -1
        my_piece = BLACK
        opp_piece = WHITE

    for r in range(ROWS):
        for c in range(COLS):
            if get_cell(board, r, c) != my_piece:
                continue
            nr = r + dr
            if nr < 0 or nr >= ROWS:
                continue
            # Forward
            if get_cell(board, nr, c) == EMPTY:
                moves.append((r, c, nr, c))
            # Capture left
            if c - 1 >= 0 and get_cell(board, nr, c - 1) == opp_piece:
                moves.append((r, c, nr, c - 1))
            # Capture right
            if c + 1 < COLS and get_cell(board, nr, c + 1) == opp_piece:
                moves.append((r, c, nr, c + 1))

    return moves


def apply_action(state: State, action: Action) -> State:
    """
    Return the new state after applying action. Does not check legality.
    """
    board, turn = state
    fr, fc, tr, tc = action
    piece = get_cell(board, fr, fc)
    # Clear from-cell and set to-cell (immutable: copy, modify, re-tuple)
    cells = list(board)
    cells[fr * COLS + fc] = EMPTY
    cells[tr * COLS + tc] = piece
    board = tuple(cells)
    return (board, -turn)
