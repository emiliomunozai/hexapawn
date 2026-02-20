"""
Entry point: train Q-learning agent on Hexapawn, then report results.

Run with: uv run python -m hexapawn.run
"""

import argparse
from hexapawn.environment import HexapawnEnv
from hexapawn.agent import QLearningAgent
from hexapawn.training import train, run_episode


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Q-learning on Hexapawn")
    parser.add_argument("--episodes", type=int, default=5000, help="Training episodes")
    parser.add_argument("--alpha", type=float, default=0.1, help="Learning rate")
    parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor")
    parser.add_argument("--epsilon", type=float, default=0.2, help="Exploration rate")
    parser.add_argument("--eval-every", type=int, default=500, help="Evaluate every N episodes")
    parser.add_argument("--eval-episodes", type=int, default=100, help="Episodes per evaluation")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    env = HexapawnEnv(agent_side=1, seed=args.seed)
    agent = QLearningAgent(alpha=args.alpha, gamma=args.gamma, epsilon=args.epsilon, seed=args.seed)

    print("Training Q-learning on Hexapawn...")
    eval_returns = train(
        env,
        agent,
        args.episodes,
        eval_every=args.eval_every,
        num_eval_episodes=args.eval_episodes,
    )
    if eval_returns:
        print(f"Evaluation average returns (every {args.eval_every} episodes):")
        for i, r in enumerate(eval_returns):
            print(f"  {args.eval_every * (i + 1)}: {r:.3f}")
        print(f"Final (last {args.eval_episodes} eval episodes): {eval_returns[-1]:.3f}")
    print(f"Q-table size: {agent.num_states()} states")


if __name__ == "__main__":
    main()
