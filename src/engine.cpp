#include "../include/engine.h"
#include <iostream>
#include <sstream>

Game::Game(const std::string& boardString, int depth, int opponent_heuristic_mode, int player_heuristic_mode) {
    this->depth = depth;
    this->opponent_heuristic_mode = opponent_heuristic_mode;
    this->player_heuristic_mode = player_heuristic_mode;

    this->rows_count = 0;
    this->col_count = 0;

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
            
            if(this->rows_count == 0) {
                this->col_count = row.size();
            } else if (row.size() != this->col_count) {
                std::cerr << "Error: Inconsistent row lengths in board string." << std::endl;
                exit(1);
            }

            this->rows_count++;

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
    for (int i = 0; i < col_count; ++i) {
        std::cout << i << ' ';
    }
    std::cout << std::endl;

    for (int idx = 0; idx < rows_count; ++idx) {
        std::cout << (idx < 10 ? " " : "") << idx << "  ";
        for (int j = 0; j < col_count; ++j) {
            std::cout << board[idx][j];
            if (j < col_count - 1) std::cout << ' ';
        }
        std::cout << std::endl;
    }
}

void Game::play(int iterations, bool is_simulation, bool should_log) {
    std::cout << "PLAYING GAME" << std::endl;
    // TODO: Implement play logic
}
