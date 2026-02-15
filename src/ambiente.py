class Hexapawn:
    """
    Ambiente simple de Hexapawn (3x3):
    - Estado: board (matriz) + turn
    - Acciones: movimientos legales ((r0,c0),(r1,c1))
    - Transición: make_move(move)
    - Terminalidad: check_winner()
    """

    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.reset()

    # -------------------------
    # ESTADO
    # -------------------------
    def _reset_board(self):
        board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        board[0] = ['B'] * self.cols
        board[self.rows - 1] = ['W'] * self.cols
        return board

    def reset(self):
        self.board = self._reset_board()
        self.turn = 'W'
        return self.get_state()

    def get_state(self):
        return {"board": [row[:] for row in self.board], "turn": self.turn}

    def display(self):
        print(f"\nTurno de: {'Blancas' if self.turn == 'W' else 'Negras'}")
        for row in self.board:
            print(" ".join(row))
        print()

    # -------------------------
    # ACCIONES
    # -------------------------
    def get_legal_moves(self, player=None):
        player = player or self.turn
        moves = []
        direction = -1 if player == 'W' else 1  # W sube, B baja

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != player:
                    continue

                nr = r + direction
                if not (0 <= nr < self.rows):
                    continue

                # 1) Avance frontal
                if self.board[nr][c] == '.':
                    moves.append(((r, c), (nr, c)))

                # 2) Capturas diagonales
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < self.cols:
                        target = self.board[nr][nc]
                        if target != '.' and target != player:
                            moves.append(((r, c), (nr, nc)))

        return moves

    # -------------------------
    # TRANSICIÓN
    # -------------------------
    def make_move(self, move):
        if move not in self.get_legal_moves(self.turn):
            raise ValueError(f"Movimiento ilegal para {self.turn}: {move}")

        (sr, sc), (er, ec) = move
        self.board[er][ec] = self.board[sr][sc]  # si hay enemigo, queda capturado
        self.board[sr][sc] = '.'

        self.turn = 'B' if self.turn == 'W' else 'W'
        return self.get_state()

    # -------------------------
    # TERMINALIDAD
    # -------------------------
    def check_winner(self):
        # 1) Coronación
        if 'W' in self.board[0]:
            return 'W'
        if 'B' in self.board[self.rows - 1]:
            return 'B'

        # 2) Sin piezas del rival (regla común; si el profe no la usa, puedes quitarla)
        flat = [cell for row in self.board for cell in row]
        if 'W' not in flat:
            return 'B'
        if 'B' not in flat:
            return 'W'

        # 3) Ahogado: jugador en turno sin movimientos => pierde
        if not self.get_legal_moves(self.turn):
            return 'W' if self.turn == 'B' else 'B'

        return None

    def is_terminal(self):
        return self.check_winner() is not None

if __name__ == "__main__":
    env = Hexapawn()
    env.display()

    moves = env.get_legal_moves()
    print("Movimientos legales:", moves)

    env.make_move(moves[0])
    env.display()


