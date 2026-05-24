#include "engine.h"
#include <iostream>

int main() {

    // width, height, depth, opponentHeuristicMode, playerHeuristicMode
    Game game(8, 8, 4, HeuristicStrategies::Balanced, HeuristicStrategies::Balanced);

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(false, true);
    
    return 0;
}
