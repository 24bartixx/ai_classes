#include "engine.h"
#include <iostream>

int main() {

    // width, height, depth, opponentHeuristicMode, playerHeuristicMode
    
    Game game(8, 8, 4, HeuristicStrategies::Aggressive, HeuristicStrategies::Defensive);

    game.display();

    // iterations, isSimulation, shouldLog
    game.play(true, true);
    
    return 0;
}
