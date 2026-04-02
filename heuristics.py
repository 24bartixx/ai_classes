def evalute_heuristic(board, player):
    score = 0
    
    for row in board:
        for cell in row:
            if cell == player:
                score += 1
            elif cell != '_' and cell != 'o':
                score -= 1
                
    return score


# importance: very high
def evaluate_sides_proximity(game, player):
    
    board = game.board
    
    proximity_weights = {
        0: 4,  
        1: 2, 
        2: 1, 
    }
    
    col_count = len(board[0]) if len(board) > 0 else 0
    
    score = 0
    opponent = 'B' if player == 'W' else 'W'
    
    for row in board:
        for i in range(col_count):
        
            size_dist = min(i, col_count - 1 - i)
            
            cell_score = proximity_weights.get(size_dist, 0)
            
            if row[i] == player:
                score += cell_score
            elif row[i] == opponent:
                score -= cell_score
                
    return score

# low importance
def evaluate_mobility(game, player):
    
    board = game.board
    
    opponent = 'B' if player == 'W' else 'W'
    player_moves = 0
    opponent_moves = 0

    for row in range(game.rows_count):
        for col in range(game.col_count):
            piece = board[row][col]
            if piece == player or piece == opponent:
                direction = -1 if piece == player else 1
                to_row = row + direction
                
                if 0 <= to_row < game.rows_count:
                    
                    # Forward
                    if board[to_row][col] == '_':
                        if piece == player:
                            player_moves += 1
                        else:
                            opponent_moves += 1
                    # Left
                    to_col_left = col - 1
                    if to_col_left >= 0:
                        if board[to_row][to_col_left] != piece and board[to_row][to_col_left] != 'o':
                            if piece == player:
                                player_moves += 1
                            else:
                                opponent_moves += 1
                    # Right
                    to_col_right = col + 1
                    if to_col_right < game.col_count:
                        if board[to_row][to_col_right] != piece and board[to_row][to_col_right] != 'o':
                            if piece == player:
                                player_moves += 1
                            else:
                                opponent_moves += 1
                                
    return player_moves - opponent_moves