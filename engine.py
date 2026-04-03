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
    
 