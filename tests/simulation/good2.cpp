#include "engine.h"
#include <iostream>

int main() {

    // width, height, depth, opponentHeuristicMode, playerHeuristicMode
    
    int depth = 5;
    Game game(8, 8, depth, HeuristicStrategies::Tournament, HeuristicStrategies::Tournament);

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
