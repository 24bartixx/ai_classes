(define (domain transport-domain)
    (:requirements :strips :typing :conditional-effects :action-costs)
    (:types
        vehicle city package
        truck train ferry - vehicle
    )

    (:predicates
        (v-at ?v - vehicle ?c - city)
        (is-truck ?v - vehicle)
        (is-train ?v - vehicle)
        (is-ferry ?v - vehicle)
        (p-at ?p - package ?c - city)
        (is-island ?c - city)
        (on-island ?p - package)
        (blocked ?c1 ?c2 - city)
        (truck-connected ?c1 ?c2 - city)
        (train-connected ?c1 ?c2 - city)
        (ferry-connected ?c1 ?c2 - city)
    )

    (:functions
        (total-cost) - number
    )

    (:action move-truck
        :parameters (?v - truck ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (truck-connected ?from ?to)
            (not (blocked ?from ?to))
        )
        :effect (and
            (not (v-at ?v ?from))
            (v-at ?v ?to)
            (increase (total-cost) 4)
        )
    )

    (:action move-train
        :parameters (?v - train ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (train-connected ?from ?to)
            (not (blocked ?from ?to))
        )
        :effect (and
            (not (v-at ?v ?from))
            (v-at ?v ?to)
            (increase (total-cost) 3)
        )
    )

    (:action move-ferry
        :parameters (?v - ferry ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (ferry-connected ?from ?to)
        )
        :effect (and
            (not (v-at ?v ?from))
            (v-at ?v ?to)
            (increase (total-cost) 2)
        )
    )

    (:action transport-truck
        :parameters (?v - truck ?p - package ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (p-at ?p ?from)
            (truck-connected ?from ?to)
            (not (blocked ?from ?to))
        )
        :effect (and
            (not (v-at ?v ?from))
            (not (p-at ?p ?from))
            (v-at ?v ?to)
            (p-at ?p ?to)
            (when (on-island ?p) (not (on-island ?p)))
            (increase (total-cost) 5)
        )
    )

    (:action transport-train
        :parameters (?v - train ?p - package ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (p-at ?p ?from)
            (train-connected ?from ?to)
            (not (blocked ?from ?to))
        )
        :effect (and
            (not (v-at ?v ?from))
            (not (p-at ?p ?from))
            (v-at ?v ?to)
            (p-at ?p ?to)
            (when (on-island ?p) (not (on-island ?p)))
            (increase (total-cost) 4)
        )
    )

    (:action transport-ferry
        :parameters (?v - ferry ?p - package ?from - city ?to - city)
        :precondition (and
            (v-at ?v ?from)
            (p-at ?p ?from)
            (ferry-connected ?from ?to)
        )
        :effect (and
            (not (v-at ?v ?from))
            (not (p-at ?p ?from))
            (v-at ?v ?to)
            (p-at ?p ?to)
            (when (is-island ?to) (on-island ?p))
            (increase (total-cost) 3)
        )
    )

)