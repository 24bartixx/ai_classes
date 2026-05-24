#include "engine.h"
#include <iostream>

int main() {

    // width, height, depth, opponentHeuristicMode, playerHeuristicMode
    // sides center proximity = 1, finish proximity = 2, material = 3, back row guard = 4, danger penalty = 5, path openness = 6
    Game game(8, 8, 4, HeuristicWeights{1, 0, 0}, HeuristicWeights{1, 0, 0});

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
