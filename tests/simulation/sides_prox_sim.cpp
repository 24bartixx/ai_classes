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

    Game game(INITIAL_BOARD, 3, 1, 1);

    game.display();
    
    return 0;
}