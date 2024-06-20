"""
Ce module contient les stratégies 
que la fontion strategy donnée au serveur doit appeler
"""
from typing import Dict, Any
from gndclient import Action, Player, State, Time

from gopher import play_randomly, strategy_gopher_mcts

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
    if time_left < 8 :
        action = play_randomly(env,state,player)
        return (env, action)
    return strategy_gopher_mcts(env,state,player,time_left)

def strategy_dodo(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """ Stratégie à appeler pour dodo"""
    print("New state ", state)
    print("Time remaining ", time_left)
    print("Player", player)

    # TO DO

    return (env, (0, 0))
