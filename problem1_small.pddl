(define (problem transport-problem-small)
    (:domain transport-domain)

    (:objects
        truck1 - truck
        city1 city2 city3 city4 city5 - city
        package1 package2 package3 package4 - package
    )

    (:init
        (t_at truck1 city3)

        (connected city1 city2)
        (connected city2 city1)
        (connected city2 city3)
        (connected city3 city2)
        (connected city3 city4)
        (connected city4 city3)
        (connected city4 city5)
        (connected city5 city4)
        (connected city2 city4)
        (connected city4 city2)
        (connected city1 city3)
        (connected city3 city1)
        (connected city3 city5)
        (connected city5 city3)

        (p_at package1 city1)
        (p_at package2 city2)
        (p_at package3 city4)
        (p_at package4 city5)

        (= (total-cost) 0)
    )

    (:goal
        (and
            (p_at package1 city4)
            (p_at package2 city4)
            (p_at package3 city2)
            (p_at package4 city4)
        )
    )

    (:metric minimize (total-cost))
)