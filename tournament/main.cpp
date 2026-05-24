#include "engine.h"
#include <iostream>
#include <limits>
#include <string>

using namespace std;

int main() {

    // print format
    cout << "1 1" << endl;

    int boardWidth, boardHeight;
    bool isWhite;
    int depth = 5;
    
    cin >> boardWidth >> boardHeight >> isWhite;
    isWhite = !isWhite;

    const HeuristicWeights tournamentWeights{5, 5, 25, 3, 10, 4};
    Game game(boardWidth, boardHeight, depth, tournamentWeights, tournamentWeights);

    if(isWhite) {
        cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        string initialBoardLine;
        getline(cin, initialBoardLine);
    }

    if(!isWhite) {
        int prev_col, prev_row, new_col, new_row;
        cin >> prev_col >> prev_row >> new_col >> new_row;
        game.makeMove(prev_row, prev_col, new_row, new_col);
    }

    while(true) {
        auto move = game.makeBestMove(isWhite);
        cout << move[1] << " " << move[0] << " " << move[3] << " " << move[2] << endl;

        int prev_col, prev_row, new_col, new_row;
        cin >> prev_col >> prev_row >> new_col >> new_row;
        game.makeMove(prev_row, prev_col, new_row, new_col);
    }
}
