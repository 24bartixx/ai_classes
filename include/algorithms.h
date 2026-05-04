// algorithms.h
#ifndef ALGORITHMS_H
#define ALGORITHMS_H


#include <climits>
#include <optional>
#include <vector>
#include <utility>
#include <string>
#include "heuristics.h"
#include "types.h"

using namespace std;

class Game;

optional<Move> getBestMove(Board& board, int depth, const HeuristicWeights& heuristicWeights, char player_color, int& visitedNodes);

int minimax(Board& board, int depth, const HeuristicWeights& heuristicWeights, char maximizing_for, bool isMaximizingPlayer, int& visitedNodes, int alpha = INT_MIN, int beta = INT_MAX);

int evaluate(Board& board, const HeuristicWeights& heuristicWeights);

bool isOver(const Board& board);

vector<Move> getLegalMoves(const Board& board, char player_color);

Position makeMove(Board& board, const Move& move);

#endif 
