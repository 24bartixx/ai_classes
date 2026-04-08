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
        col_labels = [str(i) for i in range(self.col_count)]
        
        print('\n    ', end='')
        print(' '.join(col_labels))

        for idx, row in enumerate(self.board):
            print(f"{idx:2}  ", end='')
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
                    
                    if next_move is None:
                        print("\nNo legal moves available for White.\nGame over!")
                        break
                    
                    make_move(self.board, next_move)
                else:
                    legal_moves = get_legal_moves(self.board, 'W')
                    if not legal_moves:
                        print("\nNo legal moves available for White.\nGame over!\n")
                        game_ended = True
                        break
                    
                    print("\nAvailable moves:\n")
                    
                    for idx, move in enumerate(legal_moves):
                        (from_pos, to_pos) = move
                        print(f"\t{idx + 1}:\t{from_pos} -> {to_pos}")
                        
                    while True:
                        try:
                            choice = int(input(f"\nSelect your move (1-{len(legal_moves)}): "))
                            if 1 <= choice <= len(legal_moves):
                                next_move = legal_moves[choice - 1]
                                break
                            else:
                                print("Invalid choice. Please select a valid move number.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                            
                    make_move(self.board, next_move)
                    
            else:
                if not is_simulation:
                    print("\nWaiting for AI to make its move...\n")
                    
                next_move = get_best_move(self.board, self.search_depth, self.opponent_heuristic_mode, 'B')
                
                if next_move is None:
                    print("\nNo legal moves available for Black.\nGame over!\n")
                    break
                
                make_move(self.board, next_move)
                
            current_player = 'B' if current_player == 'W' else 'W'
            i += 1
            if should_log:
                print(f"\nAfter move {i} ({'White' if current_player == 'B' else 'Black'}):\n")
                self.display()

        # Print outcome at the end
        print("\nFinal board state:")
        self.display()
        
        for i in range(self.col_count):
            if self.board[0][i] == 'W':
                print("\nWhite wins!\n")
                return
            elif self.board[self.rows_count - 1][i] == 'B':
                print("\nBlack wins!\n")
                return
            
        
        w_count = sum(row.count('W') for row in self.board)
        b_count = sum(row.count('B') for row in self.board)
        
        if w_count > b_count:
            print("\nWhite wins!\n")
        elif b_count > w_count:
            print("\nBlack wins!\n")
        else:
            print("\nDraw!\n")
            
        
    
 