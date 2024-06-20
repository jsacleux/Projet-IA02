"""
Ce module contient les stratégies 
que la fontion strategy donnée au serveur doit appeler
"""
from typing import Dict, Any
from gndclient import Action, Player, State, Time, Env

from gopher import play_randomly_gopher, strategy_gopher_mcts, get_coup_strat_opti
from dodo import strategy_dodo_mcts, play_randomly_dodo


def strategy_gopher_opt_impaire(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Cette fonction est la strategie optimisée pour le joueur 1 sur les grilles impaires """
    if env["premier_tour"]:
        env["premier_tour"] = False
        new_state = [i for i in state if i[0] != (0, 0)]
        new_state.append(((0, 0), player))
        env["Old_state"] = new_state
        return env, (0, 0)

    coup = get_coup_strat_opti(env, state, player)

    new_state = [i for i in state if i[0] != coup]
    new_state.append((coup, player))
    env["Old_state"] = new_state

    return env, coup


def strategy_gopher(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Stratégie à appeler pour une grille gopher de taille paire"""
    if time_left < 8 :
        action = play_randomly_gopher(env,state,player)
        return (env, action)
    return strategy_gopher_mcts(env,state,player,time_left)


def strategy_dodo(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Stratégie à appeler pour dodo"""
    if time_left < 8 :
        action = play_randomly_dodo(env,state,player)
        return (env, action)
    return strategy_dodo_mcts(env,state,player,time_left)
