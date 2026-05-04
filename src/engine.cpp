#include "../include/engine.h"
#include <algorithm>
#include <iostream>
#include <sstream>
#include <optional>

Game::Game(const std::string& boardString, int depth, const HeuristicWeights& playerHeuristicWeights, const HeuristicWeights& opponentHeuristicWeights)
    : depth(depth),
      opponentHeuristicWeights(opponentHeuristicWeights),
      playerHeuristicWeights(playerHeuristicWeights),
      rowsCount(0),
      colCount(0) {
    int i = 0;
    while (i < boardString.size()) {
        std::vector<char> row;

        while (i < boardString.size() && boardString[i] != '\n') {
            if(boardString[i] != ' ') {
                row.push_back(boardString[i]);
            }
            i++;
        }

        if (!row.empty()) {
            board.push_back(row);
            
            if(this->rowsCount == 0) {
                this->colCount = row.size();
            } else if (row.size() != this->colCount) {
                std::cerr << "Error: Inconsistent row lengths in board string." << std::endl;
                exit(1);
            }

            this->rowsCount++;

        }

        if (i < boardString.size() && boardString[i] == '\n') {
            i++;
        }
    }

    if(board.empty()) {
        std::cerr << "Error: Empty board string." << std::endl;
        exit(1);
    }
}

void Game::display() const {

    std::cout << "\n    ";
    for (int i = 0; i < colCount; ++i) {
        std::cout << i << ' ';
    }
    std::cout << std::endl;

    for (int idx = 0; idx < rowsCount; ++idx) {
        std::cout << (idx < 10 ? " " : "") << idx << "  ";
        for (int j = 0; j < colCount; ++j) {
            std::cout << board[idx][j];
            if (j < colCount - 1) std::cout << ' ';
        }
        std::cout << std::endl;
    }
}

void Game::play(bool isSimulation, bool shouldLog, int iterations) {
    std::cout << "\n===== PLAYING GAME =====" << std::endl;
    
    char currentPlayer = 'W';
    int i = 0;
    
    while(!isOver(board) && (iterations == -1 || i < iterations)) {
        if(currentPlayer == 'W') {

            optional<Move> nextMove;
            if(isSimulation) {
                nextMove = getBestMove(board, depth, playerHeuristicWeights, currentPlayer);

                if(!nextMove.has_value())  {
                    std::cout << "\nNo legal moves available for White.\nGame over!";
                    break;
                }

                makeMove(board, nextMove.value());
            } else {
                vector<Move> legalMoves = getLegalMoves(board, currentPlayer);

                if(legalMoves.empty()) {
                    std::cout << "\nNo legal moves available for White.\nGame over!\n";
                    break;
                }

                cout << "\nAvailable moves:\n";

                for(int i = 0; i < legalMoves.size(); i++) {
                    const Move& move = legalMoves[i];
                    cout << "\t" << i + 1 << ":\t(" << move.first.first << ", " << move.first.second << ") -> ("
                         << move.second.first << ", " << move.second.second << ")\n";
                }

                while(true) {
                    cout << "\nSelect your move (1-" << legalMoves.size() << "): ";
                    int choice;
                    cin >> choice;

                    if(choice >= 1 && choice <= legalMoves.size()) {
                        nextMove = legalMoves[choice - 1];
                        break;
                    } else {
                        cout << "Invalid input. Please enter a number.";
                    }
                }

                makeMove(board, nextMove.value());
            }
        } else {
            if(!isSimulation) {
                cout << "\nWaiting for AI to make its move...\n";
            }

            optional<Move> nextMove = getBestMove(board, depth, opponentHeuristicWeights, 'B');

            if(!nextMove.has_value()) {
                cout << "\nNo legal moves available for Black.\nGame over!\n";
                break;
            }

            makeMove(board, nextMove.value());
        }

        currentPlayer = (currentPlayer == 'W') ? 'B' : 'W';

        i++;

        if(shouldLog) {
            cout << endl << "After move " << i << " (" << currentPlayer << "):" << endl; 
            display();
        }

    }

    if(!isSimulation && isOver(board)) {
        if(count(board[0].begin(), board[0].end(), 'W') > 0) {
            cout << "\nYou win! White reached the opposite side.\n";
        } else if(count(board[board.size() - 1].begin(), board[board.size() - 1].end(), 'B') > 0) {
            cout << "\nAI wins! Black reached the opposite side.\n";
        }
    }
}
