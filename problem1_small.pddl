(define (problem transport-problem-small)
    (:domain transport-domain)

    (:objects
        truck1 truck2 - truck
        train1 train2 - train
        ferry1 - ferry
        city1 city2 city3 city4 city5 city6 - city
        package1 package2 package3 package4 package5 - package
    )

    (:init
        (is-truck truck1)
        (is-truck truck2)
        (is-train train1)
        (is-train train2)
        (is-ferry ferry1)

        (v-at truck1 city3)
        (v-at truck2 city5)
        (v-at train1 city2)
        (v-at train2 city6)
        (v-at ferry1 city1)

        (ferry-connected city1 city2)
        (ferry-connected city2 city1)
        (ferry-connected city2 city3)
        (ferry-connected city3 city2)

        (train-connected city2 city4)
        (train-connected city4 city2)
        (train-connected city2 city5)
        (train-connected city5 city2)
        (train-connected city2 city6)
        (train-connected city6 city2)
        (train-connected city5 city6)
        (train-connected city6 city5)

        (truck-connected city1 city5)
        (truck-connected city5 city1)
        (truck-connected city3 city4)
        (truck-connected city4 city3)
        (truck-connected city3 city5)
        (truck-connected city5 city3)
        (truck-connected city4 city5)
        (truck-connected city5 city4)

        (p-at package1 city1)
        (p-at package2 city4)
        (p-at package3 city6)
        (p-at package4 city2)
        (p-at package5 city5)

        (is-island city1)

        (blocked city2 city5)

        (= (total-cost) 0)
    )

    (:goal
        (and
            (on-island package1)
            (on-island package2)
            (p-at package3 city4)
            (p-at package4 city6)
            (p-at package5 city2)
        )
    )

    (:metric minimize (total-cost))
)