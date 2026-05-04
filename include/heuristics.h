#ifndef HEURISTICS_H
#define HEURISTICS_H

class HeuristicWeights {
public:
    HeuristicWeights(
        double sidesProximityWeight,
        double mobilityWeight,
        double lineCompletionWeight,
        double centerProximityWeight,
        double finishProximityWeight,
        double prioritizeCaptureWeight)
        : sidesProximityWeight(sidesProximityWeight),
          mobilityWeight(mobilityWeight),
          lineCompletionWeight(lineCompletionWeight),
          centerProximityWeight(centerProximityWeight),
          finishProximityWeight(finishProximityWeight),
          prioritizeCaptureWeight(prioritizeCaptureWeight) {}

    double getSidesProximityWeight() const { return sidesProximityWeight; }
    double getMobilityWeight() const { return mobilityWeight; }
    double getLineCompletionWeight() const { return lineCompletionWeight; }
    double getCenterProximityWeight() const { return centerProximityWeight; }
    double getFinishProximityWeight() const { return finishProximityWeight; }
    double getPrioritizeCaptureWeight() const { return prioritizeCaptureWeight; }


private:
    double sidesProximityWeight;
    double mobilityWeight;
    double lineCompletionWeight;
    double centerProximityWeight;
    double finishProximityWeight;
    double prioritizeCaptureWeight;
};

namespace HeuristicStrategies {
    inline const HeuristicWeights Defensive{5, 1, 2, 0, 0, 5};
    inline const HeuristicWeights Aggressive{0, 2, 1, 0, 5, 10};
    inline const HeuristicWeights Balanced{2, 2, 2, 2, 2, 6};
    inline const HeuristicWeights CenterControl{0, 1, 0, 5, 1, 5};
    inline const HeuristicWeights MobilityRush{0, 5, 0, 0, 0, 7};
    inline const HeuristicWeights LineBuilder{1, 0, 5, 0, 1, 6};
    inline const HeuristicWeights CaptureFocused{0, 1, 0, 0, 2, 12};
}

#endif
