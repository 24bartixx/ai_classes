#ifndef TYPES_H
#define TYPES_H

#include <vector>
#include <utility>

using Board = std::vector<std::vector<char>>;
using Position = std::pair<int, int>;
using Move = std::pair<Position, Position>;

struct GameResult {
    char winner = '_';
    int rounds = 0;
    int visitedNodes = 0;
    double elapsedSeconds = 0.0;
};

struct StrategyStats {
    int wins = 0;
    int losses = 0;
};

#endif
