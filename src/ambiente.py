class Hexpawn:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        # Representación: 'W' (Blanco), 'B' (Negro), '.' (Vacío)
        self.board = self._reset_board()
        self.turn = 'W'  # Blancas siempre empiezan

    def _reset_board(self):
        board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        board[0] = ['B'] * self.cols  # Fila superior para Negros
        board[self.rows-1] = ['W'] * self.cols  # Fila inferior para Blancas
        return board

    def display(self):
        print(f"\nTurno de: {'Blancas' if self.turn == 'W' else 'Negras'}")
        for row in self.board:
            print(" ".join(row))
        print()

    def get_legal_moves(self, player):
        moves = []
        direction = -1 if player == 'W' else 1
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == player:
                    # 1. Movimiento hacia adelante (si está vacío)
                    nr = r + direction
                    if 0 <= nr < self.rows and self.board[nr][c] == '.':
                        moves.append(((r, c), (nr, c)))
                    
                    # 2. Capturas diagonales
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            target = self.board[nr][nc]
                            if target != '.' and target != player:
                                moves.append(((r, c), (nr, nc)))
        return moves

    def make_move(self, move):
        (start_r, start_c), (end_r, end_c) = move
        self.board[end_r][end_c] = self.board[start_r][start_c]
        self.board[start_r][start_c] = '.'
        
        # Cambio de turno
        self.turn = 'B' if self.turn == 'W' else 'W'

    def check_winner(self):
        # 1. ¿Alguien llegó al final?
        if 'W' in self.board[0]: return 'W'
        if 'B' in self.board[self.rows-1]: return 'B'
        
        # 2. ¿El jugador actual se quedó sin movimientos? (Ahogado)
        if not self.get_legal_moves(self.turn):
            return 'W' if self.turn == 'B' else 'B'
            
        return None