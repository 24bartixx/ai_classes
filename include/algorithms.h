// algorithms.h
#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include <vector>
#include <utility>
#include <string>

using Board = std::vector<std::vector<char>>;
using Move = std::pair<std::pair<int, int>, std::pair<int, int>>;

Move get_best_move(const Board& board, int depth, int heuristic_mode, char player_color);

int minimax(Board board, int depth, bool is_maximizing_player, int heuristic_mode, char maximizing_for, int alpha = INT_MIN, int beta = INT_MAX);

bool is_over(const Board& board);

std::vector<Move> get_legal_moves(const Board& board, char player_color);

void make_move(Board& board, const Move& move);

#endif 
