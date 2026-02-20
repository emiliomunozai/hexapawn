"""
Agent (RL component: Learner / Policy / Value function).

Q-learning agent with:
- Q-table: Q(s, a) stored as dict[state, dict[action_index, float]]
- ε-greedy policy for exploration
- Q-update rule: Q(s,a) <- Q(s,a) + α [ r + γ max_a' Q(s',a') - Q(s,a) ]
"""

import random

from .state import State
from .actions import Action, legal_actions


class QLearningAgent:
    """
    Tabular Q-learning. Actions are indexed by position in legal_actions list,
    so we store (state, action_index) -> Q-value.
    """

    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.99,
        epsilon: float = 0.2,
        seed: int | None = None,
    ):
        self.alpha = alpha   # Learning rate
        self.gamma = gamma   # Discount factor
        self.epsilon = epsilon  # Exploration (ε-greedy)
        self._rng = random.Random(seed)
        # Q[state][action_index] = value. state is hashable; action_index is int.
        self._q: dict[State, dict[int, float]] = {}

    def _action_index(self, state: State, action: Action) -> int:
        """Index of action in legal_actions(state)."""
        legal = legal_actions(state)
        for i, a in enumerate(legal):
            if a == action:
                return i
        raise ValueError("Action not legal")

    def _get_q(self, state: State, action_index: int) -> float:
        """Return Q(state, action_index); 0.0 if unseen."""
        return self._q.get(state, {}).get(action_index, 0.0)

    def _set_q(self, state: State, action_index: int, value: float) -> None:
        if state not in self._q:
            self._q[state] = {}
        self._q[state][action_index] = value

    def _max_q(self, state: State) -> float:
        """max_a Q(s, a) for legal actions; 0.0 if no actions or unseen."""
        legal = legal_actions(state)
        if not legal:
            return 0.0
        return max(self._get_q(state, i) for i in range(len(legal)))

    def select_action(self, state: State) -> tuple[Action, int]:
        """
        ε-greedy: with probability epsilon pick random legal action,
        else pick greedy action. Returns (action, action_index).
        """
        legal = legal_actions(state)
        if not legal:
            raise ValueError("No legal actions")
        if self._rng.random() < self.epsilon:
            idx = self._rng.randint(0, len(legal) - 1)
            return legal[idx], idx
        # Greedy: break ties randomly
        best_val = self._get_q(state, 0)
        best_indices = [0]
        for i in range(1, len(legal)):
            v = self._get_q(state, i)
            if v > best_val:
                best_val = v
                best_indices = [i]
            elif v == best_val:
                best_indices.append(i)
        idx = self._rng.choice(best_indices)
        return legal[idx], idx

    def update(
        self,
        state: State,
        action_index: int,
        reward: float,
        next_state: State,
        done: bool,
    ) -> None:
        """
        Q-learning update:
          Q(s,a) <- Q(s,a) + α [ r + γ max_a' Q(s',a') - Q(s,a) ]
        If done, max_a' Q(s',a') = 0.
        """
        q_old = self._get_q(state, action_index)
        if done:
            target = reward
        else:
            target = reward + self.gamma * self._max_q(next_state)
        q_new = q_old + self.alpha * (target - q_old)
        self._set_q(state, action_index, q_new)

    def num_states(self) -> int:
        """Number of states ever seen (for logging)."""
        return len(self._q)
