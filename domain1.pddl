(define (domain transport-domain)
    (:requirements :strips :typing :action-costs)
    (:types truck city package)

    (:predicates
        (t_at ?truck ?city)
        (p_at ?package ?city)
        (connected ?c1 ?c2 - city)
    )

    (:functions
        (total-cost) - number
    )

    (:action move
        :parameters (?t - truck ?from - city ?to - city)
        :precondition (and 
            (t_at ?t ?from) 
            (connected ?from ?to)
        )
        :effect (and
            (not (t_at ?t ?from))
            (t_at ?t ?to)
            (increase (total-cost) 3)
        )
    )

    (:action transport
        :parameters (?t - truck ?p - package ?from - city ?to - city )
        :precondition (and
            (t_at ?t ?from)
            (p_at ?p ?from)
            (connected ?from ?to)
        )
        :effect (and
            (not (t_at ?t ?from))
            (not (p_at ?p ?from))
            (t_at ?t ?to)
            (p_at ?p ?to)
            (increase (total-cost) 5)
        )
    )

)