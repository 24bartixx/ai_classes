from algorithms import *


class Game:
    def __init__(self, board_string, search_depth, opponent_heuristic_mode, player_heuristic_mode):
        
        self.opponent_heuristic_mode = opponent_heuristic_mode
        self.player_heuristic_mode = player_heuristic_mode
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
    
    
    def play(self, iterations = None, is_simulation = False, should_log = False):
        
        current_player = 'W'
        
        i = 0
        
        while not is_over(self.board) and (iterations is None or i < iterations):
            
            if current_player == 'W':
        
                if is_simulation:
                    next_move = get_best_move(self.board, self.search_depth, self.player_heuristic_mode, 'W')
                    make_move(self.board, next_move)
                
                else:
                    # TODO: get move from user input
                    raise NotImplementedError("User input move is not implemented yet.")
                    
            else:
                next_move = get_best_move(self.board, self.search_depth, self.opponent_heuristic_mode, 'B')
                make_move(self.board, next_move)
                
            current_player = 'B' if current_player == 'W' else 'W'
            i += 1
            
            if should_log:
                print(f"\nAfter move {i} ({'White' if current_player == 'B' else 'Black'}):\n")
                self.display()
            
        
    
 