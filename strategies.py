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
    """ Cette fonction est la strategie optimisée pour le joueur 1 sur les grilles impaires.
     Ainsi, si nous sommes le joueur 1 sur une grille de taille impaire, nous gagnons.
     Cette fonction n'est appelée qu'à cette condition. """


    if env["premier_tour"]: # Le premier coup est toujours le même, et nous permet d'initialiser notre attribut "old_state"
                            # de notre environnement
        env["premier_tour"] = False
        new_state = [i for i in state if i[0] != (0, 0)]
        new_state.append(((0, 0), player))
        env["Old_state"] = new_state
        return env, (0, 0)

    coup = get_coup_strat_opti(env, state, player) # appel à la fonction qui trouve le coup à jouer

    new_state = [i for i in state if i[0] != coup] # mise à jour de l'environnement
    new_state.append((coup, player))
    env["Old_state"] = new_state

    return env, coup


def strategy_gopher(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Stratégie de gopher, utilisant la méthode MCTS pour trouver le meilleur coup à jouer.
    Si il reste moins de 8 secondes à la partie, nous jouons au hasard parmis les coups légaux,
    pour ne pas perdre contre la montre."""
    if time_left < 8 :
        action = play_randomly_gopher(env,state,player)
        return (env, action)
    return strategy_gopher_mcts(env,state,player,time_left)


def strategy_dodo(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Stratégie de dodo, utilisant la méthode MCTS pour trouver le meilleur coup à jouer.
    Si il reste moins de 8 secondes à la partie, nous jouons au hasard parmis les coups légaux,
    pour ne pas perdre contre la montre."""
    if time_left < 8 :
        action = play_randomly_dodo(env,state,player)
        return (env, action)
    return strategy_dodo_mcts(env,state,player,time_left)
