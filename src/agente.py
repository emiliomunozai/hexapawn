# agente.py
import random

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {} 
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q_table.get(str(state), {}).get(str(action), 0.0)

    def choose_action(self, state, legal_moves):
        if random.random() < self.epsilon:
            return random.choice(legal_moves)
        qs = [self.get_q(state, a) for a in legal_moves]
        max_q = max(qs)
        best_actions = [a for a, q in zip(legal_moves, qs) if q == max_q]
        return random.choice(best_actions)

    def learn(self, s, a, r, s_prime, next_legal_moves, done):
        s_key = str(s)
        a_key = str(a)
        if s_key not in self.q_table:
            self.q_table[s_key] = {}
        
        current_q = self.get_q(s_key, a_key)
        
        if done:
            target = r
        else:
            next_qs = [self.get_q(s_prime, m) for m in next_legal_moves]
            target = r + self.gamma * (max(next_qs) if next_qs else 0)
            
        self.q_table[s_key][a_key] = current_q + self.alpha * (target - current_q)