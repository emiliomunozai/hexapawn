"""
Environment (RL component: MDP / World).

The environment implements the Markov Decision Process:
- States (see state.py)
- Actions (see actions.py)
- Transitions: step(state, action) -> (next_state, reward, done)
- Initial state: reset() -> state

We only step when it's the agent's turn; when it's the opponent's turn
we use a simple policy (e.g. random) to get the next state.
"""

import random

from .state import State, initial_state, WHITE, BLACK
from .actions import legal_actions, apply_action, Action
from .reward import is_terminal, reward_for_agent


class HexapawnEnv:
    """
    Hexapawn MDP. Agent plays one side (default: White).
    Opponent plays the other side (e.g. random).
    """

    def __init__(self, agent_side: int = WHITE, seed: int | None = None):
        self.agent_side = agent_side
        self._rng = random.Random(seed)
        self._state: State | None = None

    def reset(self) -> State:
        """Return initial state (always white to move)."""
        self._state = initial_state()
        # If agent is black, advance one step with a random white move.
        while self._state is not None and self._current_turn() != self.agent_side:
            self._state = self._step_opponent(self._state)
        assert self._state is not None
        return self._state

    def _current_turn(self) -> int:
        assert self._state is not None
        return self._state[1]

    def _step_opponent(self, state: State) -> State:
        """One step by opponent (random move). Returns new state."""
        moves = legal_actions(state)
        if not moves:
            return state
        action = self._rng.choice(moves)
        return apply_action(state, action)

    def opponent_move(self, state: State) -> tuple[Action | None, State]:
        """Opponent picks a move from state. Returns (action, next_state). No moves → (None, state)."""
        moves = legal_actions(state)
        if not moves:
            return (None, state)
        action = self._rng.choice(moves)
        return (action, apply_action(state, action))

    def step(self, action: Action) -> tuple[State, float, bool]:
        """
        Agent takes action. Returns (next_state, reward, done).
        If not done and next turn is opponent, we auto-apply opponent move
        so the next state is again agent's turn (or terminal).
        """
        if self._state is None:
            raise RuntimeError("Call reset() first")
        state = self._state
        next_state = apply_action(state, action)
        done = is_terminal(next_state)
        reward = reward_for_agent(next_state, self.agent_side) if done else 0.0

        if not done and next_state[1] != self.agent_side:
            next_state = self._step_opponent(next_state)
            done = is_terminal(next_state)
            if done:
                reward = reward_for_agent(next_state, self.agent_side)

        self._state = next_state
        return next_state, reward, done

    def legal_actions(self, state: State | None = None) -> list:
        """Legal actions for current player in state (default: current env state)."""
        s = state if state is not None else self._state
        if s is None:
            return []
        return legal_actions(s)
