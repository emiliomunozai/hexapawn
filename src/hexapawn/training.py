"""
Training loop (RL component: Agent–Environment interaction).

Runs episodes: reset -> while not done: agent selects action, env steps, agent updates.
"""

from .environment import HexapawnEnv
from .agent import QLearningAgent
from .state import State
from .actions import Action, apply_action
from .reward import is_terminal, reward_for_agent


def simulate_step_by_step(
    env: HexapawnEnv,
    agent: QLearningAgent,
    *,
    train: bool = False,
    max_steps: int = 100,
):
    """
    Generator that yields **one move at a time** (agent or opponent).
    Each yield: (state, action, next_state, reward, done, is_agent_move).
    So you see: state → action → next_state; then next_state becomes the next state → action → ...
    No jumps: every state is either the initial state or the "next_state" from the previous move.
    """
    state = env.reset()
    for _ in range(max_steps):
        legal = env.legal_actions(state)
        if not legal:
            if is_terminal(state):
                yield state, None, state, reward_for_agent(state, env.agent_side), True, False
            break
        if state[1] == env.agent_side:
            # Agent's turn (Player 1 / White when agent_side==1)
            action, action_index = agent.select_action(state)
            next_state = apply_action(state, action)
            assert next_state[1] == -state[1], "turn must flip after move"
            done = is_terminal(next_state)
            reward = reward_for_agent(next_state, env.agent_side) if done else 0.0
            yield state, action, next_state, reward, done, True
            if train:
                full_next, _, _ = env.step(action)
                agent.update(state, action_index, reward, full_next, done)
                state = full_next
            else:
                env._state = next_state
                state = next_state
            if done:
                break
        else:
            # Opponent's turn (Player 2 / Black when agent_side==1)
            action, next_state = env.opponent_move(state)
            if action is None:
                break
            assert next_state[1] == -state[1], "turn must flip after move"
            done = is_terminal(next_state)
            reward = reward_for_agent(next_state, env.agent_side) if done else 0.0
            env._state = next_state
            yield state, action, next_state, reward, done, False
            state = next_state
            if done:
                break


def run_episode(
    env: HexapawnEnv,
    agent: QLearningAgent,
    *,
    train: bool = True,
) -> tuple[float, int]:
    """
    Run one episode. Returns (total_reward, step_count).
    If train=True, agent is updated after each step.
    """
    state = env.reset()
    total_reward = 0.0
    steps = 0

    while True:
        legal = env.legal_actions(state)
        if not legal:
            if steps == 0 and is_terminal(state):
                total_reward = reward_for_agent(state, env.agent_side)
            break
        action, action_index = agent.select_action(state)
        next_state, reward, done = env.step(action)
        total_reward += reward
        steps += 1
        if train:
            agent.update(state, action_index, reward, next_state, done)
        state = next_state
        if done:
            break

    return total_reward, steps


def train(
    env: HexapawnEnv,
    agent: QLearningAgent,
    num_episodes: int,
    *,
    eval_every: int | None = None,
    num_eval_episodes: int = 50,
) -> list[float]:
    """
    Train for num_episodes. If eval_every is set, run evaluation
    (no exploration) every eval_every episodes and return list of
    average evaluation returns for plotting.
    """
    eval_returns: list[float] = []
    agent_was_epsilon = agent.epsilon
    try:
        for episode in range(num_episodes):
            run_episode(env, agent, train=True)
            if eval_every and (episode + 1) % eval_every == 0:
                agent.epsilon = 0.0
                returns = [
                    run_episode(env, agent, train=False)[0]
                    for _ in range(num_eval_episodes)
                ]
                eval_returns.append(sum(returns) / len(returns))
                agent.epsilon = agent_was_epsilon
    finally:
        agent.epsilon = agent_was_epsilon
    return eval_returns
