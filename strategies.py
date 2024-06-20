"""
Ce module contient les stratégies 
que la fontion strategy donnée au serveur doit appeler
"""
from typing import Dict, Any
from gndclient import Action, Player, State, Time

Environment = Dict[str, Any]


def strategy_gopher_optimale(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """" Stratégie optimale apellee pour une grille gopher de taille impaire"""
    print("New state ", state)
    print("Time remaining ", time_left)
    print("Player", player)

    # TO DO

    return (env, (0, 0))


def strategy_gopher(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """ Stratégie à appeler pour une grille gopher de taille paire"""
    print("New state ", state)
    print("Time remaining ", time_left)
    print("Player", player)

    # TO DO

    return (env, (0, 0))


def strategy_dodo(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """ Stratégie à appeler pour dodo"""
    print("New state ", state)
    print("Time remaining ", time_left)
    print("Player", player)

    # TO DO

    return (env, (0, 0))
