"""
Ce fichier permet de se connecter au serveur et de jouer
"""

#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from gndclient import (
    start,
    Env,
    Action,
    Score,
    Player,
    State,
    Time,
    DODO_STR,
    GOPHER_STR,
)

from strategies import strategy_dodo, strategy_gopher, strategy_gopher_opt_impaire
from gopher import premier_tour, strategy_gopher_mcts
from dodo import strategy_dodo_mcts


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Env:
    """ Cette fonction est appelée au début de la partie"""
    print("Init")
    print(
        f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )

    env: Dict[str, Any] = {}
    env["game"] = game
    env["hex_size"] = hex_size
    env["us"] = player
    env["premier_tour"] = premier_tour(state) # un attribut booléen pour savoir si le tour est le premier.
    if game == GOPHER_STR:
        env["n_simulations"] = 2000 # le nombre de simulation pour notre MCTS de gopher
    else:
        env["n_simulations"] = 1000  # le nombre de simulation pour notre MCTS de gopher
    return env


def strategy_brain(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Fonction pour jouer en tant qu'humain. N'est jamais utilisé ici."""
    print("New state ", player)
    print("New state ", state)
    print("Time remaining ", time_left)
    print("What's your play ? ", end="")
    s = input()
    t = ast.literal_eval(s)
    return (env, t)


def strategy(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """
    Nous appelons cette fonction quel que soit le jeu et les conditions de la partie.
    Elle nous permet de faire le choix entre les différentes stratégies que nous avons crées.
    La stratégie appelée est la même tout au long d'une même partie.
    """
    if env["game"] == GOPHER_STR:
        if env["hex_size"] % 2 == 1 and player == 1:
            return strategy_gopher_opt_impaire(env, state, player, time_left)
        return strategy_gopher(env, state, player, time_left)
    if env["game"] == DODO_STR:
        return strategy_dodo(env, state, player, time_left)
    return (env, (0, 0))


def final_result(state: State, score: Score, player: Player):
    """
    Cette fonction est appelee à la fin de la partie
    """
    print(f"Ending: {player} wins")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://lagrue.ninja/")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize,
        strategy,
        final_result,
        gui=True,
    )
