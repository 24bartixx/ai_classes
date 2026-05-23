#include "engine.h"
#include <iostream>

int main() {

    std::string INITIAL_BOARD = 
        "W W W W W W W W\n"
        "W W W W W W W W\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "_ _ _ _ _ _ _ _\n"
        "B B B B B B B B\n"
        "B B B B B B B B\n";

    // initialBoard, depth, opponentHeuristicMode, playerHeuristicMode
    Game game(INITIAL_BOARD, 4, HeuristicStrategies::LineBuilder, HeuristicStrategies::LineBuilder);

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(false, true);
    
    return 0;
}
