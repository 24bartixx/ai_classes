#include "engine.h"
#include <iostream>

int main() {

    std::string INITIAL_BOARD = 
        "B B B B B B B B\n"
        "B B B B B B B B\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "W W W W W W W W\n"
        "W W W W W W W W\n";

    // initialBoard, depth, opponentHeuristicMode, playerHeuristicMode
    // sides proximity = 1, mobility = 2, line completion = 3
    Game game(INITIAL_BOARD, 3, HeuristicWeights{0, 1, 0}, HeuristicWeights{0, 1, 0});

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
