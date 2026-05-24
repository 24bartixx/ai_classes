#include "engine.h"
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <map>
#include <streambuf>
#include <string>
#include <vector>

using namespace std;

struct StrategyEntry {
    string name;
    HeuristicWeights weights;
};

class NullBuffer : public streambuf {
public:
    int overflow(int character) override {
        return character;
    }
};

class StreamSilencer {
public:
    StreamSilencer(ostream& stream, streambuf* replacement)
        : stream(stream), original(stream.rdbuf(replacement)) {}

    ~StreamSilencer() {
        stream.rdbuf(original);
    }

private:
    ostream& stream;
    streambuf* original;
};

void recordResult(
    const GameResult& result,
    const StrategyEntry& white,
    const StrategyEntry& black,
    map<string, StrategyStats>& stats) {
    if(result.winner == 'W') {
        stats[white.name].wins++;
        stats[black.name].losses++;
    } else if(result.winner == 'B') {
        stats[black.name].wins++;
        stats[white.name].losses++;
    }
}

string winnerName(const GameResult& result, const StrategyEntry& white, const StrategyEntry& black) {
    if(result.winner == 'W') {
        return white.name + " (White)";
    }

    if(result.winner == 'B') {
        return black.name + " (Black)";
    }

    return "None";
}

GameResult playMatch(
    const StrategyEntry& white,
    const StrategyEntry& black) {
    cout << "Starting: " << white.name << " (White) vs "
         << black.name << " (Black)" << endl;

    NullBuffer nullBuffer;

    Game game(8, 8, 4, white.weights, black.weights);
    GameResult result;

    {
        StreamSilencer silenceCout(cout, &nullBuffer);
        StreamSilencer silenceCerr(cerr, &nullBuffer);
        result = game.play(true, false);
    }

    cout << "Finished: " << white.name << " (White) vs "
         << black.name << " (Black)"
         << " | Winner: " << winnerName(result, white, black)
         << " | Rounds: " << result.rounds
         << " | Time: " << fixed << setprecision(3)
         << result.elapsedSeconds << "s" << endl;

    return result;
}

int main() {
    vector<StrategyEntry> strategies = {
        {"Defensive", HeuristicStrategies::Defensive},
        {"Aggressive", HeuristicStrategies::Aggressive},
        {"Balanced", HeuristicStrategies::Balanced},
        {"SidesCenterControl", HeuristicStrategies::SidesCenterControl},
        {"FinishRush", HeuristicStrategies::FinishRush},
        {"MaterialFocused", HeuristicStrategies::MaterialFocused},
        {"BackRowGuard", HeuristicStrategies::BackRowGuard},
        {"PathOpenness", HeuristicStrategies::PathOpenness}
    };

    map<string, StrategyStats> stats;
    int gamesPlayed = 0;
    int totalRounds = 0;
    int totalVisitedNodes = 0;
    double totalElapsedSeconds = 0.0;

    for(const StrategyEntry& strategy : strategies) {
        stats[strategy.name] = StrategyStats{};
    }

    for(int i = 0; i < strategies.size(); i++) {
        for(int j = i + 1; j < strategies.size(); j++) {
            GameResult first = playMatch(strategies[i], strategies[j]);
            recordResult(first, strategies[i], strategies[j], stats);

            GameResult second = playMatch(strategies[j], strategies[i]);
            recordResult(second, strategies[j], strategies[i], stats);

            gamesPlayed += 2;
            totalRounds += first.rounds + second.rounds;
            totalVisitedNodes += first.visitedNodes + second.visitedNodes;
            totalElapsedSeconds += first.elapsedSeconds + second.elapsedSeconds;
        }
    }

    cout << "\n===== STRATEGY TOURNAMENT =====\n";
    cout << "Games played: " << gamesPlayed << "\n";
    cout << "Total rounds: " << totalRounds << "\n";
    cout << "Total visited nodes: " << totalVisitedNodes << "\n";
    cout << fixed << setprecision(3);
    cout << "Total simulation time: " << totalElapsedSeconds << " seconds\n\n";

    vector<StrategyEntry> sortedStrategies = strategies;
    sort(sortedStrategies.begin(), sortedStrategies.end(),
        [&](const StrategyEntry& first, const StrategyEntry& second) {
            const StrategyStats& firstStats = stats[first.name];
            const StrategyStats& secondStats = stats[second.name];

            if(firstStats.wins != secondStats.wins) {
                return firstStats.wins > secondStats.wins;
            }

            return firstStats.losses < secondStats.losses;
        });

    cout << left
         << setw(18) << "Strategy"
         << right
         << setw(8) << "Wins"
         << setw(8) << "Losses" << "\n";
    cout << string(34, '-') << "\n";

    for(const StrategyEntry& strategy : sortedStrategies) {
        const StrategyStats& strategyStats = stats[strategy.name];
        cout << left << setw(18) << strategy.name
             << right
             << setw(8) << strategyStats.wins
             << setw(8) << strategyStats.losses << "\n";
    }

    cout << "\n\n";

    return 0;
}
