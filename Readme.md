# Hexapawn With Reinforcement Learning

A repository for exploring **Reinforcement Learning (RL)** using [Hexapawn](https://en.wikipedia.org/wiki/Hexapawn): a minimal game ideal for understanding MDPs, value functions, and Q-learning in a small, interpretable setting.


## Why Hexapawn?

- **Tiny state and action space** — easy to inspect Q-tables and policies.
- **Fast episodes** — quick iteration for courses and experiments.
- **Clear RL concepts** — environment, agent, reward, and training loop map directly to the code.

## What You'll Find Here

The code is split into **theoretical RL components** so you can open one module at a time during a course:

| Component | Role in RL | Where in code |
|-----------|------------|----------------|
| **Environment** | MDP: states, actions, transitions, “game rules” | `src/hexapawn/environment.py` |
| **State** | State representation (hashable for tabular methods) | `src/hexapawn/state.py` |
| **Actions** | Action space / legal moves from a state | `src/hexapawn/actions.py` |
| **Reward** | Reward function \(R(s, a, s')\) | `src/hexapawn/reward.py` |
| **Agent** | Learner: Q-table, policy (e.g. ε-greedy), Q-update | `src/hexapawn/agent.py` |
| **Training** | Episodes, steps, agent–environment interaction | `src/hexapawn/training.py` |

Run the default Q-learning training and evaluation from the project root:

```bash
uv run python -m hexapawn.run
```

Or install and run the CLI:

```bash
uv sync
hexapawn
```

## State space and action space (how they are defined)

**State space**  
A state must fully describe the situation for the agent to choose an action. We use:

- **Board:** 3×3 grid, row by row. Each cell is `0` (empty), `1` (white pawn), or `-1` (black pawn). Stored as a **tuple of 9 integers** (row-major) so it is hashable for the Q-table.
- **Turn:** whose move it is: `1` (white) or `-1` (black).

So a state is `(board_tuple, turn)`. Example: initial game is `((1,1,1, 0,0,0, -1,-1,-1), 1)`.

**Action space**  
An action is a single move. We encode it as **from-cell and to-cell**:

- **Action:** `(from_row, from_col, to_row, to_col)`.

From a given state, only some actions are legal (current player’s pawns, empty or enemy target). So the **action space is state-dependent**: we define `legal_actions(state)` as the list of these 4-tuples. Pawns move **forward one square** (if empty) or **capture diagonally forward**; no backward moves. The agent’s Q-table indexes actions by their position in `legal_actions(state)` (0, 1, 2, …) so the same “move” can have different indices in different states.

## Notebooks

Open `notebooks/01_qlearning_hexapawn.ipynb` and select the project’s `.venv` as the kernel. The notebook includes a **step-by-step simulation**: a generator you advance with `next(sim)` in repeated cells to see each state and action one at a time.

## Project Layout

```
hexapawn/
├── README.md           # This file
├── pyproject.toml
├── notebooks/          # Example + simulation
│   └── 01_qlearning_hexapawn.ipynb
├── src/
│   └── hexapawn/
│       ├── __init__.py
│       ├── state.py      # State representation
│       ├── actions.py    # Action space / legal moves
│       ├── reward.py     # Reward function
│       ├── environment.py # MDP / game logic
│       ├── agent.py      # Q-learning agent
│       ├── training.py   # Training loop
│       ├── run.py        # Entry point (train + eval)
│       └── cli.py        # CLI (optional)
```

## Algorithm: Q-Learning

We use **tabular Q-learning** with:

- **Q(s, a)** stored in a dictionary (state → action → value).
- **Update rule:**  
  $$
  Q(s,a) \leftarrow Q(s,a) + \alpha \bigl[ r + \gamma \max_{a'} Q(s',a') - Q(s,a) \bigr]
  $$
- **ε-greedy** exploration during training.

You can follow the flow: `environment` produces states and rewards, `agent` chooses actions and updates Q, and `training` runs episodes.

## Setup

- **Python:** 3.12.5
- **Install:** `uv sync` (or `pip install -e .`)

See `uv_guide.md` for UV setup on Windows.

## Course Use

1. Start with **state** and **actions** to see how we represent the game.
2. Add **reward** and **environment** to complete the MDP.
3. Introduce **agent** (Q-table and update rule).
4. Wire everything in **training** and **run** to watch the agent learn.