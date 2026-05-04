#include "engine.h"
#include "algorithms.h"
#include <iostream>


using namespace std;

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

    Game game(INITIAL_BOARD, 4, HeuristicWeights{1, 1, 1, 0}, HeuristicWeights{1, 1, 1, 0});
    cout << "Initial board :" << endl; // hej tu Oleńka
    game.display();

    vector<Move> moves = getLegalMoves(game.getBoard(), 'B');

    cout << "\nLegal moves for player B:" << endl;
    for(const Move& move : moves) {
       cout << "Legal move: (" << move.first.first << ", " << move.first.second << ") -> ("
                  << move.second.first << ", " << move.second.second << ")" << endl;
    }

    char currentPlayer = 'W';
    for(int i = 0; i < 10; i++) {
        vector<Move> legalMoves = getLegalMoves(game.getBoard(), currentPlayer);
        if (legalMoves.empty()) {
            cout << "No legal moves available for player " << currentPlayer << "." << endl;
            break;
        }

        Move randomMove = legalMoves[rand() % legalMoves.size()];

        makeMove(game.getBoard(), randomMove);

        cout << "\nAfter move " << i + 1 << " by player " << currentPlayer << ":" << endl;
        game.display();

        int score = evaluate(game.getBoard(), HeuristicWeights{1, 1, 1, 0});
        cout << endl << "Evaluation score: " << score << endl;

        currentPlayer = (currentPlayer == 'W') ? 'B' : 'W';
    }



    return 0;

}
