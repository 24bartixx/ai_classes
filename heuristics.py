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
def evaluate_sides_proximity(board, player):
    
    board = board
    
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
def evaluate_mobility(board, player):
    
    rows_count = len(board)
    col_count = len(board[0]) if rows_count > 0 else 0
    
    opponent = 'B' if player == 'W' else 'W'
    player_moves = 0
    opponent_moves = 0

    for row in range(rows_count):
        for col in range(col_count):
            piece = board[row][col]
            if piece == player or piece == opponent:
                direction = -1 if piece == player else 1
                to_row = row + direction
                
                if 0 <= to_row < rows_count:
                    
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
                    if to_col_right < col_count:
                        if board[to_row][to_col_right] != piece and board[to_row][to_col_right] != 'o':
                            if piece == player:
                                player_moves += 1
                            else:
                                opponent_moves += 1
                                
    return player_moves - opponent_moves


# low importance
def evaluate_line_completion(board, player):    
    rows_count = len(board)
    cols_count = len(board[0]) if rows_count > 0 else 0
    
    opponent = 'B' if player == 'W' else 'W'
    
    score = 0

    def count_consecutive(line, who):
        n = len(line)
        result = 0
        i = 0
        while i < n:
            if line[i] == who:
                length = 1
                while i + length < n and line[i + length] == who:
                    length += 1
                if length >= 3:
                    result += (length - 2)
                i += length
            else:
                i += 1
        return result

    # Check all rows
    for row in board:
        for who, sign in [(player, 1), (opponent, -1)]:
            score += sign * count_consecutive(row, who)

    # Check all columns
    for col in range(cols_count):
        col_vals = [board[row][col] for row in range(rows_count)]
        for who, sign in [(player, 1), (opponent, -1)]:
            score += sign * count_consecutive(col_vals, who)

    # Check diagonals (top-left to bottom-right)
    for d in range(-(rows_count - 3), cols_count - 2):
        diag = []
        for row in range(rows_count):
            col = row + d
            if 0 <= col < cols_count:
                diag.append(board[row][col])
        for who, sign in [(player, 1), (opponent, -1)]:
            score += sign * count_consecutive(diag, who)

    # Check diagonals (top-right to bottom-left)
    for d in range(2, rows_count + cols_count - 2):
        diag = []
        for row in range(rows_count):
            col = d - row
            if 0 <= col < cols_count:
                diag.append(board[row][col])
        for who, sign in [(player, 1), (opponent, -1)]:
            score += sign * count_consecutive(diag, who)

    return score