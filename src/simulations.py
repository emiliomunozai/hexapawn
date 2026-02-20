import random
import ambiente 
import agente
from agente import QLearningAgent

class RandomAgen:
    def choose_action(self, state, legal_moves):
        return random.choice(legal_moves)

class Trainer:
    def __init__(self, env, agent_w, agent_b):
        self.env = env
        self.agent_w = agent_w
        self.agent_b = agent_b
        
    def play_episode(self, train=True):
        state = self.env.reset()
        done = False
        winner = 0
        
        # Guardar los ultimos estados para el aprendizaje terminal
        last_exp = {1: None, -1: None} 

        while not done:
            p_actual = self.env.turn
            a_actual = self.agent_w if p_actual == 1 else self.agent_b
            moves = self.env.get_legal_moves(p_actual)
            if not moves:
                winner = -p_actual
                done = True
                break

            action = a_actual.choose_action(state, moves)
            last_exp[p_actual] = (state, action) # Guardar la experiencia
            
            next_state, _, done, winner = self.env.step(action)
            
            if train:
                # Si el agente tiene el método learn, LLAMARLO. Sin isinstance ni validaciones extra.
                if hasattr(a_actual, 'learn'):
                    prox_moves = self.env.get_legal_moves(self.env.turn)
                    # Si el juego terminó en este paso, la recompensa es 1
                    reward = 1 if (done and winner == p_actual) else 0
                    a_actual.learn(state, action, reward, next_state, prox_moves, done)
            
            state = next_state

        # Si el juego termino y alguien perdio, avisarle al agente
        if train and winner != 0:
            perdedor = -winner
            a_perdedor = self.agent_w if perdedor == 1 else self.agent_b
            if hasattr(a_perdedor, 'learn') and last_exp[perdedor]:
                s_old, a_old = last_exp[perdedor]
                # enviamos un -1 al que perdio
                a_perdedor.learn(s_old, a_old, -1, state, [], True)
            
        return winner


class DebugTrainer(Trainer):
    def play_episode(self, train=True):
        ganador = super().play_episode(train)
        return ganador

# Creamos el ambiente y agente
env = ambiente.HexapawnEnv()
rl_agent = agente.QLearningAgent(alpha=0.1, epsilon=0.3)
trainer = DebugTrainer(env, rl_agent, RandomAgen())

print("Iniciando el entrenamiento completo")
for i in range(5000):
    trainer.play_episode(train=True)

print("Evaluando...")
rl_agent.epsilon = 0 # Apagamos exploración
wins = 0
tests = 1000
for _ in range(tests):
    if trainer.play_episode(train=False) == 1:
        wins += 1

print(f"Tasa de aprendizaje: {wins/tests * 100}%")
print(f"Tamaño de la Q-Table: {len(rl_agent.q_table)} estados")

# Entendiendo la politica

print("\n ANALIZANDO LA ESTRATEGIA APRENDIDA ")
# Creamos el estado inicial exacto
estado_inicial = env.reset()

print("Tablero Inicial:")
trainer.print_board()

# Obtenemos todos los valores Q para el estado inicial
movimientos_iniciales = env.get_legal_moves(1)
print("Valores Q para el primer movimiento:")

mejor_q = -float('inf')
mejor_movimiento = None

for mov in movimientos_iniciales:
    # Nuestro agente guarda las acciones como strings -> convertimos el movimiento a string para consultar la Q-table
    q_valor = rl_agent.get_q(estado_inicial, mov)
    print(f"Movimiento {mov}: Recompensa Esperada = {q_valor:.3f}")
    
    if q_valor > mejor_q:
        mejor_q = q_valor
        mejor_movimiento = mov

print(f"\nPolítica Óptima π*(s_0): El agente prefiere el movimiento {mejor_movimiento}")