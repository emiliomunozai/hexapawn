"""
Reward function (RL component: Reward).

R(s, a, s') or R(s') for terminal states. We use outcome-based rewards:
- Win: +1
- Loss: -1
- Draw: 0 (optional; in Hexapawn draws are rare)

We need to know who the "agent" is (e.g. White). Reward is from the agent's perspective.
"""

from .state import State, WHITE, BLACK
from .actions import legal_actions


def is_terminal(state: State) -> bool:
    """True if the game is over (win, loss, or draw)."""
    board, turn = state
    moves = legal_actions(state)
    if moves:
        return False
    # No legal moves: current player lost (other player wins)
    return True


def winner(state: State) -> int | None:
    """
    If game is terminal: 1 = white won, -1 = black won, 0 = draw.
    If not terminal, returns None.
    """
    if not is_terminal(state):
        return None
    _, turn = state
    # The player who had to move had no moves, so the other player won.
    return -turn


def reward_for_agent(
    next_state: State,
    agent_side: int,
    *,
    win: float = 1.0,
    loss: float = -1.0,
    draw: float = 0.0,
) -> float:
    """
    Reward from the agent's perspective when transitioning to next_state.
    Only meaningful when next_state is terminal.
    """
    w = winner(next_state)
    if w is None:
        return 0.0
    if w == 0:
        return draw
    if w == agent_side:
        return win
    return loss
