#ifndef ENGINE_H
#define ENGINE_H

#include <vector>
#include <string>
#include "algorithms.h"

class Game {
public:
    Game(const std::string& board_string, int depth, int opponent_heuristic_mode, int player_heuristic_mode);
    void display() const;
    void play(int iterations = -1, bool is_simulation = false, bool should_log = false);

private:
    Board board;

    int depth;
    int opponent_heuristic_mode;
    int player_heuristic_mode;
    
    int rows_count;
    int col_count;
};

#endif
