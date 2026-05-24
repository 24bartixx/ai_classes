#ifndef ENGINE_H
#define ENGINE_H


#include <array>
#include <vector>
#include <string>
#include "types.h"
#include "algorithms.h"

class Game {
public:
    Game(const std::string& board_string, int depth, const HeuristicWeights& playerHeuristicWeights, const HeuristicWeights& opponentHeuristicWeights);
    Game(int width, int height, int depth, const HeuristicWeights& playerHeuristicWeights, const HeuristicWeights& opponentHeuristicWeights);
    void display() const;
    GameResult play(bool isSimulation = false, bool shouldLog = false, int iterations = -1);
    void makeMove(int prev_row, int prev_col, int new_row, int new_col);
    std::array<int, 4> makeBestMove(bool isWhite);

    Board& getBoard() { return board; }
    const Board& getBoard() const { return board; }    
    int getRowsCount() const { return rowsCount; }
    int getColCount() const { return colCount; }

private:
    Board board;

    int depth;
    HeuristicWeights opponentHeuristicWeights;
    HeuristicWeights playerHeuristicWeights;

    int rowsCount;
    int colCount;
};

#endif
