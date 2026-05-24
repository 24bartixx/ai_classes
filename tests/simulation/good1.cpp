#include "engine.h"
#include <iostream>

int main() {
    // width, height, depth, opponentHeuristicMode, playerHeuristicMode

    // sides proximity = 1
    // mobility = 2
    // line completion = 3
    // center proximity = 4
    // finish proximity = 5
    // prioritize capture = 6

    Game game(8, 8, 4, HeuristicWeights{5, 2, 1, 0, 0, 0}, HeuristicWeights{0, 1, 2, 3, 0, 0});

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
