#ifndef HEURISTICS_H
#define HEURISTICS_H

class HeuristicWeights {
public:
    HeuristicWeights(
        double sidesCenterProximityWeight,
        double finishProximityWeight,
        double materialWeight,
        double backRowGuardWeight = 0,
        double dangerPenaltyWeight = 0,
        double pathOpennessWeight = 0)
        : sidesCenterProximityWeight(sidesCenterProximityWeight),
          finishProximityWeight(finishProximityWeight),
          materialWeight(materialWeight),
          backRowGuardWeight(backRowGuardWeight),
          dangerPenaltyWeight(dangerPenaltyWeight),
          pathOpennessWeight(pathOpennessWeight) {}

    double getSidesCenterProximityWeight() const { return sidesCenterProximityWeight; }
    double getFinishProximityWeight() const { return finishProximityWeight; }
    double getMaterialWeight() const { return materialWeight; }
    double getBackRowGuardWeight() const { return backRowGuardWeight; }
    double getDangerPenaltyWeight() const { return dangerPenaltyWeight; }
    double getPathOpennessWeight() const { return pathOpennessWeight; }


private:
    double sidesCenterProximityWeight;
    double finishProximityWeight;
    double materialWeight;
    double backRowGuardWeight;
    double dangerPenaltyWeight;
    double pathOpennessWeight;
};


// sides center proximity = 1
// finish proximity = 2
// material = 3
// back row guard = 4
// danger penalty = 5
// path openness = 6

namespace HeuristicStrategies {
    inline const HeuristicWeights Defensive{5, 1, 20, 6, 12, 3};
    inline const HeuristicWeights Aggressive{0, 5, 18, 1, 8, 5};
    inline const HeuristicWeights Balanced{2, 2, 20, 3, 10, 4};
    inline const HeuristicWeights SidesCenterControl{5, 0, 15, 2, 8, 4};
    inline const HeuristicWeights FinishRush{0, 5, 12, 1, 6, 5};
    inline const HeuristicWeights MaterialFocused{0, 1, 30, 1, 8, 3};
    inline const HeuristicWeights BackRowGuard{0, 0, 12, 8, 6, 2};
    inline const HeuristicWeights PathOpenness{0, 1, 12, 1, 6, 10};
}

#endif
