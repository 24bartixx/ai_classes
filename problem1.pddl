(define (problem transport-problem)
    (:domain transport-domain)

    (:objects
        truck1 truck2 truck3 - truck
        city1 city2 city3 city4 city5 city6 city7 - city
        package1 package2 package3 package4 package5 package6 package7 package8 package9 - package
    )

    (:init
        (t_at truck1 city2)
        (t_at truck2 city5)
        (t_at truck3 city1)

        (connected city1 city2)
        (connected city2 city1)
        (connected city2 city3)
        (connected city3 city2)
        (connected city3 city4)
        (connected city4 city3)
        (connected city4 city5)
        (connected city5 city4)
        (connected city5 city6)
        (connected city6 city5)
        (connected city6 city7)
        (connected city7 city6)
        (connected city2 city5)
        (connected city5 city2)
        (connected city3 city6)
        (connected city6 city3)

        (p_at package1 city4)
        (p_at package2 city4)
        (p_at package3 city1)
        (p_at package4 city2)
        (p_at package5 city3)
        (p_at package6 city6)
        (p_at package7 city5)
        (p_at package8 city7)
        (p_at package9 city1)
    )

    (:goal
        (and
            (p_at package1 city7)
            (p_at package2 city1)
            (p_at package3 city5)
            (p_at package4 city3)
            (p_at package5 city6)
            (p_at package6 city2)
            (p_at package7 city4)
            (p_at package8 city2)
            (p_at package9 city7)
        )
    )

)