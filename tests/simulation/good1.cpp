#include "engine.h"
#include <iostream>

int main() {
    // width, height, depth, opponentHeuristicMode, playerHeuristicMode

    // sides center proximity = 1
    // finish proximity = 2
    // material = 3
    // back row guard = 4
    // danger penalty = 5
    // path openness = 6

    int depth = 5;
    Game game(8, 8, depth, {8, 6, 20, 3, 10, 4}, {10, 5, 20, 6, 10, 4});

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
