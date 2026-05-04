#ifndef ENGINE_H
#define ENGINE_H


#include <vector>
#include <string>
#include "types.h"
#include "algorithms.h"

class Game {
public:
    Game(const std::string& board_string, int depth, int opponent_heuristic_mode, int player_heuristic_mode);
    void display() const;
    void play(bool isSimulation = false, bool shouldLog = false, int iterations = -1);

    Board& getBoard() { return board; }
    const Board& getBoard() const { return board; }    
    int getRowsCount() const { return rowsCount; }
    int getColCount() const { return colCount; }

private:
    Board board;

    int depth;
    int opponentHeuristicMode;
    int playerHeuristicMode;
    
    int rowsCount;
    int colCount;
};

#endif
