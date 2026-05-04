
#include "../include/algorithms.h"
#include "../include/engine.h"

#include <algorithm>
#include <climits>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <map>

using namespace std;

static void clearLastMoveMarkers(Board& board) {
    for(vector<char>& row : board) {
        for(char& cell : row) {
            if(cell == 'o') {
                cell = '_';
            }
        }
    }
}

optional<Move> getBestMove(Board& board, int depth, const HeuristicWeights& heuristicWeights, char player_color, int& visitedNodes) {
    vector<Move> legalMoves = getLegalMoves(board, player_color);
    if(legalMoves.empty()) {
        return nullopt;
    }

    Move bestMove = legalMoves[0];
    int maxEval = INT_MIN;

    for(const Move& move : legalMoves) {
        Board tempBoard = board;
        clearLastMoveMarkers(tempBoard);
        makeMove(tempBoard, move);

        int eval = minimax(tempBoard, depth - 1, heuristicWeights, player_color, false, visitedNodes);
        if(eval > maxEval) {
            maxEval = eval;
            bestMove = move;
        }
    }


    return bestMove;
}

int minimax(Board& board, int depth, const HeuristicWeights& heuristicWeights, char maximizing_for, bool isMaximizingPlayer, int& visitedNodes, int alpha, int beta) {
    visitedNodes++;
    
    if(isOver(board) || depth == 0) {
        return evaluate(board, heuristicWeights);
    }

    if(isMaximizingPlayer) {
        int maxEval = INT_MIN;
        vector<Move> legalMoves = getLegalMoves(board, maximizing_for);
        if(legalMoves.empty()) {
            return INT_MIN + 1;
        }
        
        for(const Move& move : legalMoves) {
            Board tempBoard = board;
            clearLastMoveMarkers(tempBoard);
            makeMove(tempBoard, move);

            int eval = minimax(tempBoard, depth - 1, heuristicWeights, maximizing_for, false, visitedNodes, alpha, beta);
            maxEval = max(maxEval, eval);

            alpha = max(alpha, eval);
            if(beta <= alpha) break;
        }

        return maxEval;

    } else {
        int minEval = INT_MAX;
        char minimizing_for = (maximizing_for == 'B') ? 'W' : 'B';

        vector<Move> legalMoves = getLegalMoves(board, minimizing_for);
        if(legalMoves.empty()) {
            return INT_MAX - 1;
        }

        for(const Move& move : legalMoves) {
            Board tempBoard = board; 
            clearLastMoveMarkers(tempBoard);
            makeMove(tempBoard, move);

            int eval = minimax(tempBoard, depth - 1, heuristicWeights, maximizing_for, true, visitedNodes, alpha, beta);
            minEval = min(minEval, eval);

            beta = min(beta, eval);
            if(beta <= alpha) break; 
            
        }
        return minEval;
    }

    return 0;
}

// ===== IMPORTANCE =====
// High: SIDES_PROXIMITY
// Medium: 
// Low: MOBILITY, LINE_COMPLETION
// Very low: CENTER PROXIMITY

int evaluate(Board& board, const HeuristicWeights& heuristicWeights)  {

    // COMMON
    int colSize = board[0].size();
    int rowSize = board.size();

    // SIDES PROXIMITY
    map<int, int> sidesProximityWeights = {
        {0, 4},
        {1, 2},
        {2, 1}
    };

    int sidesWeight = heuristicWeights.getSidesProximityWeight();
    int sidesScore = 0;

    // MOBILITY 
    int mobilityWeight = heuristicWeights.getMobilityWeight();
    int mobilityScore = 0;

    // LINE COMPLETION
    int lineCompletionWeight = heuristicWeights.getLineCompletionWeight();
    int lineCompletionScore = 0;

    // CENTER PROXIMITY
    double rowCenter = (rowSize - 1) / 2.0;
    double colCenter = (colSize - 1) / 2.0;

    double maxDist = hypot(rowCenter, colCenter);

    int centerProximityWeight = heuristicWeights.getCenterProximityWeight();
    double centerProximityScore = 0;

    // FINISH PROXIMITY
    map<int, int> finishProximityWeights = {
        {1, 10},
        {2, 3},
        {3, 1}
    };

    int finishProximityWeight = heuristicWeights.getFinishProximityWeight();
    int finishProximityScore = 0;

    // PRIORITIZE CAPTURE
    int prioritizeCaptureWeight = heuristicWeights.getPrioritizeCaptureWeight();
    int prioritizeCaptureScore = 0;

    if(sidesWeight > 0 || mobilityWeight > 0 || centerProximityWeight > 0 
            || finishProximityWeight > 0 || prioritizeCaptureWeight > 0) {
        for(int i = 0; i < board.size(); i++) {
            for(int j = 0; j < board[i].size(); j++) {

                char cell = board[i][j];

                
                if(cell == 'B' || cell == 'W') {
                    // SIDES PROXIMITY
                    if(sidesWeight > 0) {
                        int sizeDist = min(i, colSize - 1 - i);

                        int cellScore = (sizeDist <= 2) 
                            ? sidesProximityWeights[sizeDist] 
                            : 0;

                        if(cell == 'B') sidesScore += cellScore;
                        else sidesScore -= cellScore;
                    }

                    // MOBILITY 
                    if(mobilityWeight > 0) {
                        int direction = (cell == 'B') ? 1 : -1;
                        int toRow = i + direction;

                        if (toRow >= 0 && toRow < rowSize) {

                        // Forward
                            if (board[toRow][j] == '_') {
                                if(cell == 'W') mobilityScore++;
                                else mobilityScore--;
                            }

                            // Left
                            if (j - 1 >= 0 && board[toRow][j - 1] != 'o' && board[toRow][j - 1] != cell) {
                                if(cell == 'W') mobilityScore++;
                                else mobilityScore--;
                            }

                            // Right
                            if (j + 1 < colSize && board[toRow][j + 1] != 'o' && board[toRow][j + 1] != cell) {
                                if(cell == 'W') mobilityScore++;
                                else mobilityScore--;
                            }
                        }
                    }
                
                    // CENTER PROXIMITY
                    if(centerProximityWeight > 0) {
                        double dist = hypot(rowCenter - i, colCenter - j);
                        double proximity = maxDist - dist;
                        
                        if(cell == 'W') {
                            centerProximityScore += proximity;
                        } else {
                            centerProximityScore -= proximity;
                        }
                    }

                    // FINISH PROXIMITY
                    if(finishProximityWeight > 0) {

                        if(cell == 'W') {
                            if(i > 0 && i < 4) {
                                finishProximityScore += finishProximityWeights[i];
                            }
                        } else {
                            int finishProximity = rowSize - i - 1;
                            if(finishProximity > 0 && finishProximity < 4) {
                                finishProximityScore -= finishProximityWeights[finishProximity];
                            }
                        }
                    }

                    // PRIORITIZE CAPTURE
                    if(prioritizeCaptureWeight > 0) {
                        if(cell == 'W') { 
                            if(i > 0) {
                                if((j-1 >= 0 &&board[i-1][j-1] == 'B') 
                                        || (j + 1 < colSize && board[i-1][j+1] == 'B')) {
                                    prioritizeCaptureScore += 1;

                                }
                            }
                        } else {
                            if(i < rowSize - 1) {
                                if((j-1 >= 0 && board[i+1][j-1] == 'W') 
                                        || (j + 1 < colSize && board[i+1][j+1] == 'W')) {
                                    prioritizeCaptureScore -= 1;
                                }
                            }
                        }
                    }
                    
                } 
            }
        }
    }
    
    if(lineCompletionWeight > 0) {
        // check rows
        int i = 0;
        while (i < board.size()) {
            int j = 0;
            while (j < board[i].size() - 2) {
                if(board[i][j] == 'W') {
                    if(board[i][j + 1] == 'W' && board[i][j + 2] == 'W') {
                        lineCompletionScore += 1;
                    }
                } else if(board[i][j] == 'B') {
                    if(board[i][j + 1] == 'B' && board[i][j + 2] == 'B') {
                        lineCompletionScore -= 1;
                    } 
                }
                j++;
            }
            i++;
        }

        // check columns 
        i = 0;
        while (i < board[0].size()) {
            int j = 0;
            while (j < board.size() - 2) {
                if(board[j][i] == 'W') {
                    if(board[j + 1][i] == 'W' && board[j + 2][i] == 'W') {
                        lineCompletionScore += 1;
                    }
                } else if(board[j][i] == 'B') {
                    if(board[j + 1][i] == 'B' && board[j + 2][i] == 'B') {
                        lineCompletionScore -= 1;
                    } 
                }
                j++;
            }
            i++;
        }
        
        // check top-left to bottom-right
        i = 0;
        while(i < board.size() - 2) {
            int j = 0;
            while(j < board[i].size() - 2) {
                if(board[i][j] == 'W') {
                    if(board[i + 1][j + 1] == 'W' && board[i + 2][j + 2] == 'W') {
                        lineCompletionScore += 1;
                    }
                } else if(board[i][j] == 'B') {
                    if(board[i + 1][j + 1] == 'B' && board[i + 2][j + 2] == 'B') {
                        lineCompletionScore -= 1;
                    } 
                }
                j++;
            }
            i++;
        }

        // check top-right to bottom-left
        i = 0;
        while(i < board.size() - 2) {
            int j = board[i].size() - 1;
            while(j > 1) {
                if(board[i][j] == 'W') {
                    if(board[i + 1][j - 1] == 'W' && board[i + 2][j - 2] == 'W') {
                        lineCompletionScore += 1;
                    }
                } else if(board[i][j] == 'B') {
                    if(board[i + 1][j - 1] == 'B' && board[i + 2][j - 2] == 'B') {
                        lineCompletionScore -= 1;
                    } 
                }
                j--;
            }
            i++;
        }
    }

    return sidesWeight * sidesScore 
         + mobilityWeight * mobilityScore 
         + lineCompletionWeight * lineCompletionScore
         + centerProximityWeight * centerProximityScore
         + finishProximityWeight * finishProximityScore
         + prioritizeCaptureWeight * prioritizeCaptureScore;
}

bool isOver(const Board& board) {
    if(count(board[0].begin(), board[0].end(), 'W') > 0 ||
        count(board[board.size() - 1].begin(), board[board.size() - 1].end(), 'B') > 0) {
            return true;
    }
    return false;
}

vector<Move> getLegalMoves(const Board& board, char playerColor) {
    if (playerColor != 'B' && playerColor != 'W') {
        throw invalid_argument("Invalid player color. Must be 'B' or 'W'.");
    }

    vector<Move> legalMoves;
    const int rowsCount = board.size();
    const int colCount = rowsCount > 0 ? board[0].size() : 0;

    int direction = 1;
    if (playerColor == 'W') {
        direction = -1;
    }   

    char enemy = (playerColor == 'B') ? 'W' : 'B';

    for(int row = 0; row < rowsCount; row++) {
        for(int col = 0; col < colCount; col++) {
            if (board[row][col] == playerColor) {

                int toRow = row + direction;

                if (toRow >= 0 && toRow < rowsCount) {

                    // Forward
                    if (board[toRow][col] == '_') {
                        legalMoves.push_back({{row, col}, {toRow, col}});
                    }

                    // Left
                    if (col - 1 >= 0 && (board[toRow][col - 1] == '_' || board[toRow][col - 1] == enemy)) {
                        legalMoves.push_back({{row, col}, {toRow, col - 1}});
                    }
                    // Check right diagonal
                    if (col + 1 < colCount && (board[toRow][col + 1] == '_' || board[toRow][col + 1] == enemy)) {
                        legalMoves.push_back({{row, col}, {toRow, col + 1}});
                    }
                }
            }
        }
    }

    return legalMoves;
}

Position makeMove(Board& board, const Move& move) {
    const int fromRow = move.first.first;
    const int fromCol = move.first.second;
    const int toRow = move.second.first;
    const int toCol = move.second.second;

    if(
        !(fromRow >= 0 
            && fromRow < board.size() 
            && fromCol >= 0 
            && fromCol < board[0].size() 
            && toRow >= 0 && toRow < board.size() 
            && toCol >= 0 && toCol < board[0].size())) {
        throw invalid_argument("Move is out of board bounds.");
    }

    char piece = board[fromRow][fromCol];
    if(piece != 'B' && piece != 'W') {
        throw invalid_argument("No piece at the source position.");
    }

    board[toRow][toCol] = piece;
    board[fromRow][fromCol] = 'o';

    return {fromRow, fromCol};
}
