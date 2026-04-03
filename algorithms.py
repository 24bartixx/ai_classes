from heuristics import *

def get_best_move(board, depth, heuristic_mode, player_color):
    
    best_move = None
    max_eval = float('-inf')
    
    legal_moves = get_legal_moves(board, player_color)
    
    for move in legal_moves:
        new_board = [row[:] for row in board]
        make_move(new_board, move)
        
        current_eval = minmax(new_board, depth - 1, False, heuristic_mode, player_color)
        
        if current_eval > max_eval:
            max_eval = current_eval
            best_move = move
            
    return best_move


def minmax(board, depth, is_maximizing_player, heuristic_mode, maximizing_for):
    
    if depth == 0 or is_over(board):
        match heuristic_mode:
            case 'sides_proximity':
                return evaluate_sides_proximity(board, maximizing_for)
            case 'mobility':
                return evaluate_mobility(board, maximizing_for)
            case 'line_completion':
                return evaluate_line_completion(board, maximizing_for)
    
    if is_maximizing_player:
        max_eval = float('-inf')
        
        legal_moves = get_legal_moves(board, maximizing_for)
        
        for legal_move in legal_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, legal_move)
            
            eval = minmax(new_board, depth - 1, False, heuristic_mode, maximizing_for)
            
            max_eval = max(max_eval, eval)
            
        return max_eval
    
    else:
        min_eval = float('inf')
        
        opponent_color = 'B' if maximizing_for == 'W' else 'W'
        legal_moves = get_legal_moves(board, opponent_color)
        
        for legal_move in legal_moves:
            new_board = [row[:] for row in board]
            make_move(new_board, legal_move)
            
            eval = minmax(new_board, depth - 1, True, heuristic_mode, maximizing_for)
            
            min_eval = min(min_eval, eval)
            
        return min_eval
        
        
def is_over(board):
    if board[0].count('W') > 0 or board[-1].count('B') > 0:
        return True
    
    return False


def get_legal_moves(board, player_color):
    if player_color not in {'B', 'W'}:
        raise ValueError("player_color must be 'B' or 'W'")
    
    rows_count = len(board)
    col_count = len(board[0]) if len(board) > 0 else 0

    moves = []

    direction = -1 if player_color == 'W' else 1
    enemy = 'B' if player_color == 'W' else 'W'

    for row in range(rows_count):
        for col in range(col_count):
            if board[row][col] == player_color:
                from_pos = (row, col)
                to_row = row + direction
                
                if 0 <= to_row < rows_count:
                    
                    # Forward
                    if board[to_row][col] == '_':
                        moves.append((from_pos, (to_row, col)))
                        
                    # Left
                    to_col_left = col - 1
                    if to_col_left >= 0:
                        if board[to_row][to_col_left] in {enemy, '_'}:
                            moves.append((from_pos, (to_row, to_col_left)))
                            
                    # Right
                    to_col_right = col + 1
                    if to_col_right < col_count:
                        if board[to_row][to_col_right] in {enemy, '_'}:
                            moves.append((from_pos, (to_row, to_col_right)))
    return moves


def make_move(board, move):
    
        (from_row, from_col), (to_row, to_col) = move
        rows_count = len(board)
        col_count = len(board[0]) if rows_count > 0 else 0
        
        if not (0 <= from_row < rows_count and 0 <= from_col < col_count):
            raise ValueError("Invalid from position.")
        if not (0 <= to_row < rows_count and 0 <= to_col < col_count):
            raise ValueError("Invalid to position.")
        
        piece = board[from_row][from_col]
        if piece not in {'B', 'W'}:
            raise ValueError("No movable piece at from position.")
        
        board[to_row][to_col] = piece
        board[from_row][from_col] = '_'
    


        
        
    