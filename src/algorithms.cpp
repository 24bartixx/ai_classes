
#include "../include/algorithms.h"
#include "../include/engine.h"

#include <algorithm>
#include <climits>
#include <stdexcept>

using namespace std;

static constexpr int WIN_SCORE = 9999999;
static constexpr int SIDES_CENTER_COLUMN_SCORE = 1;
static constexpr int MAX_FINISH_PROXIMITY = 2;
static constexpr int FINISH_PROXIMITY_WEIGHTS[MAX_FINISH_PROXIMITY + 1] = {0, 10, 3};
static constexpr int BACK_ROW_GUARD_MIN = 4;
static constexpr int BACK_ROW_GUARD_CAP = 5;

static void clearLastMoveMarkers(Board& board) {
    for(vector<char>& row : board) {
        for(char& cell : row) {
            if(cell == 'o') {
                cell = '_';
            }
        }
    }
}

static int getForwardDirection(char playerColor) {
    if(playerColor == 'W') {
        return -1;
    }

    if(playerColor == 'B') {
        return 1;
    }

    throw invalid_argument("Invalid player color. Must be 'B' or 'W'.");
}

static int getFinishRow(const Board& board, char playerColor) {
    return playerColor == 'W' ? 0 : static_cast<int>(board.size()) - 1;
}

static bool hasReachedFinish(const Board& board, char playerColor) {
    const int finishRow = getFinishRow(board, playerColor);
    return count(board[finishRow].begin(), board[finishRow].end(), playerColor) > 0;
}

static int getBackRowGuardScore(int piecesOnBackRow) {
    if(piecesOnBackRow >= BACK_ROW_GUARD_CAP) {
        return BACK_ROW_GUARD_CAP;
    }

    if(piecesOnBackRow == BACK_ROW_GUARD_MIN) {
        return BACK_ROW_GUARD_MIN;
    }

    int missingPieces = BACK_ROW_GUARD_MIN - piecesOnBackRow;
    return -(missingPieces * missingPieces);
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
        char sideToMove = isMaximizingPlayer ? maximizing_for : (maximizing_for == 'B' ? 'W' : 'B');
        return evaluate(board, heuristicWeights, maximizing_for, sideToMove);
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

int evaluate(Board& board, const HeuristicWeights& heuristicWeights, char maximizingFor, char sideToMove)  {

    if(count(board[0].begin(), board[0].end(), 'W') > 0) {
        return maximizingFor == 'W' ? WIN_SCORE : -WIN_SCORE;
    }

    if(count(board[board.size() - 1].begin(), board[board.size() - 1].end(), 'B') > 0) {
        return maximizingFor == 'B' ? WIN_SCORE : -WIN_SCORE;
    }

    // COMMON
    int colSize = board[0].size();
    int rowSize = board.size();

    // SIDES CENTER PROXIMITY
    int sidesCenterWeight = heuristicWeights.getSidesCenterProximityWeight();
    int sidesCenterScore = 0;
    int leftCenterCol = (colSize - 1) / 2;
    int rightCenterCol = colSize / 2;

    int finishProximityWeight = heuristicWeights.getFinishProximityWeight();
    int finishProximityScore = 0;

    // MATERIAL
    int materialWeight = heuristicWeights.getMaterialWeight();
    int materialScore = 0;

    // BACK ROW GUARD
    int backRowGuardWeight = heuristicWeights.getBackRowGuardWeight();
    int whiteBackRowPieces = 0;
    int blackBackRowPieces = 0;

    // DANGER PENALTY
    int dangerPenaltyWeight = heuristicWeights.getDangerPenaltyWeight();
    int dangerPenaltyScore = 0;

    // PATH OPENNESS
    int pathOpennessWeight = heuristicWeights.getPathOpennessWeight();
    int pathOpennessScore = 0;

    for(int i = 0; i < board.size(); i++) {
        for(int j = 0; j < board[i].size(); j++) {

            char cell = board[i][j];

            if(cell == 'B' || cell == 'W') {
                // MATERIAL
                if(cell == 'W') materialScore++;
                else materialScore--;

                // DANGER PENALTY
                if(cell != sideToMove) {
                    int attackerRow = i - getForwardDirection(sideToMove);
                    bool canBeCaptured = attackerRow >= 0 && attackerRow < rowSize
                        && ((j - 1 >= 0 && board[attackerRow][j - 1] == sideToMove)
                            || (j + 1 < colSize && board[attackerRow][j + 1] == sideToMove));

                    if(canBeCaptured) {
                        if(sideToMove == maximizingFor) dangerPenaltyScore++;
                        else dangerPenaltyScore--;
                    }
                }

                // PATH OPENNESS
                int pathDirection = getForwardDirection(cell);
                int piecesAhead = 0;

                for(int aheadRow = i + pathDirection; aheadRow >= 0 && aheadRow < rowSize; aheadRow += pathDirection) {
                    if(board[aheadRow][j] == 'W' || board[aheadRow][j] == 'B') {
                        piecesAhead++;
                    }
                }

                int pathCellScore = piecesAhead == 0 ? 1 : -piecesAhead;
                if(cell == 'W') pathOpennessScore += pathCellScore;
                else pathOpennessScore -= pathCellScore;

                // BACK ROW GUARD
                if(cell == 'W' && i == rowSize - 1) {
                    whiteBackRowPieces++;
                } else if(cell == 'B' && i == 0) {
                    blackBackRowPieces++;
                }

                // SIDES CENTER PROXIMITY
                bool isSidesCenterCol = j == 0 || j == colSize - 1 
                    || j == leftCenterCol || j == rightCenterCol;

                int cellScore = isSidesCenterCol ? SIDES_CENTER_COLUMN_SCORE : 0;

                if(cell == 'W') sidesCenterScore += cellScore;
                else sidesCenterScore -= cellScore;

                // FINISH PROXIMITY
                if(cell == 'W') {
                    int finishProximity = i;
                    if(finishProximity > 0 && finishProximity <= MAX_FINISH_PROXIMITY) {
                        finishProximityScore += FINISH_PROXIMITY_WEIGHTS[finishProximity];
                    }
                } else {
                    int finishProximity = rowSize - i - 1;
                    if(finishProximity > 0 && finishProximity <= MAX_FINISH_PROXIMITY) {
                        finishProximityScore -= FINISH_PROXIMITY_WEIGHTS[finishProximity];
                    }
                }
                
            } 
        }
    }

    int backRowGuardScore = getBackRowGuardScore(whiteBackRowPieces)
        - getBackRowGuardScore(blackBackRowPieces);

    int whitePerspectiveScore = sidesCenterWeight * sidesCenterScore 
        + finishProximityWeight * finishProximityScore
        + materialWeight * materialScore
        + backRowGuardWeight * backRowGuardScore
        + pathOpennessWeight * pathOpennessScore;

    int relativeScore = maximizingFor == 'W' ? whitePerspectiveScore : -whitePerspectiveScore;

    return relativeScore + dangerPenaltyWeight * dangerPenaltyScore;
}

bool isOver(const Board& board) {
    if(hasReachedFinish(board, 'W') || hasReachedFinish(board, 'B')) {
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

    int direction = getForwardDirection(playerColor);

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
