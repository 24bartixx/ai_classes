#ifndef TYPES_H
#define TYPES_H

#include <vector>
#include <utility>

using Board = std::vector<std::vector<char>>;
using Position = std::pair<int, int>;
using Move = std::pair<Position, Position>;

#endif
