class Game:
    def __init__(self, board_string, heuristic_mode, search_depth):
        
        self.heuristic_mode = heuristic_mode
        self.search_depth = search_depth
        
        self.board = []
        
        lines = [line.strip() for line in board_string.strip().split('\n') if line.strip()]
        
        expected_length = None
        for idx, line in enumerate(lines):
            row = line.split()
            
            if expected_length is None:
                expected_length = len(row)
            elif len(row) != expected_length:
                raise ValueError(f"Row {idx+1} has inconsistent length: expected {expected_length}, got {len(row)}")
            for symbol in row:
                if symbol not in {'B', 'W', '_', 'o'}:
                    raise ValueError(f"Invalid symbol '{symbol}' in board string.")
                
            self.board.append(row)
            
        self.rows_count = len(self.board)
        self.col_count = expected_length if self.board else 0
        if self.rows_count == 0 or self.col_count == 0:
            raise ValueError("Board must have at least one row and one column.")
        
    def display(self):
        for row in self.board:
            print(' '.join(row))

    def __repr__(self):
        return '\n'.join(' '.join(row) for row in self.board)
    
    
    
    
def get_legal_moves(game, player_color):
    if player_color not in {'B', 'W'}:
        raise ValueError("player_color must be 'B' or 'W'")

    moves = []

    direction = -1 if player_color == 'W' else 1
    enemy = 'B' if player_color == 'W' else 'W'

    for row in range(game.rows_count):
        for col in range(game.col_count):
            if game.board[row][col] == player_color:
                from_pos = (row, col)
                to_row = row + direction
                
                if 0 <= to_row < game.rows_count:
                    
                    # Forward
                    if game.board[to_row][col] == '_':
                        moves.append((from_pos, (to_row, col)))
                        
                    # Left
                    to_col_left = col - 1
                    if to_col_left >= 0:
                        if game.board[to_row][to_col_left] in {enemy, '_'}:
                            moves.append((from_pos, (to_row, to_col_left)))
                            
                    # Right
                    to_col_right = col + 1
                    if to_col_right < game.col_count:
                        if game.board[to_row][to_col_right] in {enemy, '_'}:
                            moves.append((from_pos, (to_row, to_col_right)))
    return moves

def make_move(game, move):
        (from_row, from_col), (to_row, to_col) = move
        
        if not (0 <= from_row < game.rows_count and 0 <= from_col < game.col_count):
            raise ValueError("Invalid from position.")
        if not (0 <= to_row < game.rows_count and 0 <= to_col < game.col_count):
            raise ValueError("Invalid to position.")
        
        piece = game.board[from_row][from_col]
        if piece not in {'B', 'W'}:
            raise ValueError("No movable piece at from position.")
        
        game.board[to_row][to_col] = piece
        game.board[from_row][from_col] = '_'
    
