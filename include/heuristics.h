#ifndef HEURISTICS_H
#define HEURISTICS_H

class HeuristicWeights {
public:
    HeuristicWeights(
        double sidesProximityWeight,
        double mobilityWeight,
        double lineCompletionWeight,
        double centerProximityWeight)
        : sidesProximityWeight(sidesProximityWeight),
          mobilityWeight(mobilityWeight),
          lineCompletionWeight(lineCompletionWeight),
          centerProximityWeight(centerProximityWeight) {}

    double getSidesProximityWeight() const { return sidesProximityWeight; }
    double getMobilityWeight() const { return mobilityWeight; }
    double getLineCompletionWeight() const { return lineCompletionWeight; }
    double getCenterProximityWeight() const { return centerProximityWeight; }


private:
    double sidesProximityWeight;
    double mobilityWeight;
    double lineCompletionWeight;
    double centerProximityWeight;
};

#endif
