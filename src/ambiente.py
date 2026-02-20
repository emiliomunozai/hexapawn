import random
import numpy as np

class HexapawnEnv:
    #Hexapawn, implementacion del ambiente dentro de un escenario de RL.
    def __init__(self):
        self.reset()

    def reset(self):
        # 1: White (Agente 1)
        # -1: Black (Agente 2)
        # 0: Vacio
        self.board = np.array([
            [ 1,  1,  1],
            [ 0,  0,  0],
            [-1, -1, -1]
        ])
        self.turn = 1 # Empieza blanco
        return self.get_state_string()

    def get_state_string(self):
        return "".join(map(str, self.board.flatten()))

    def get_legal_moves(self, player):
        moves = []
        direction = 1 if player == 1 else -1 # White se mueve hacia arriba (+row), Black se mueve hacia abajo (-row)
        
        for r in range(3):
            for c in range(3):
                if self.board[r, c] == player:
                    # Movimiento hacia adelante
                    nr = r + direction
                    if 0 <= nr < 3 and self.board[nr, c] == 0:
                        moves.append(((r, c), (nr, c)))
                    # Movimiento de captura diagonal
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nr < 3 and 0 <= nc < 3:
                            if self.board[nr, nc] == -player:
                                moves.append(((r, c), (nr, nc)))
        return moves

    def step(self, action):
        # Movimiento que ejecuta un agente. Una accion esta, por lo tanto, dentro de: ((r1, c1), (r2, c2))"""
        (r1, c1), (r2, c2) = action
        self.board[r2, c2] = self.board[r1, c1]
        self.board[r1, c1] = 0
        
        # Validar condiciones de victoria o derrota
        winner = self.check_winner()
        self.turn *= -1 # Pasar el turno al otro jugador
        
        reward = 1 if winner != 0 else 0
        done = winner != 0
        return self.get_state_string(), reward, done, winner

    def check_winner(self):
            # 1. Llegar a la zona final (end zone)
            # El Blanco (1) avanza hacia abajo, gana si toca la fila 2
            if 1 in self.board[2, :]: return 1
            
            # El Negro (-1) avanza hacia arriba, gana si toca la fila 0
            if -1 in self.board[0, :]: return -1
            
            # 2. Sin movimientos para el jugador actual (Stalemate)
            if not self.get_legal_moves(-self.turn): return self.turn
            
            return 0