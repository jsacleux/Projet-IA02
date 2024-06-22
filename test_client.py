"""
Ce fichier permet de se connecter au serveur et de jouer
"""

#!/usr/bin/python3

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
from gopher import premier_tour


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Env:
    """Cette fonction est appelée au début de la partie"""
    print("Init")
    print(
        f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )

    env: Dict[str, Any] = {}

    env["game"] = game  # gopher ou dodo
    env["hex_size"] = hex_size  # taille de la grille
    env["us"] = player  # notre joueur
    env["premier_tour"] = premier_tour(
        state
    )  # Booléen pour savoir si c'est le premier tour
    if game == GOPHER_STR:
        env["n_simulations"] = 2000  # Nombre de simulations pour notre MCTS de gopher
    else:
        env["n_simulations"] = 1000  # Nombre de simulations pour notre MCTS de dodo
    return env


def strategy(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """
    Cette fonction est la stratégie que nous fournissons à la fonction start.
    Elle détermine quelle stratégie appliquer en fonction du jeu
    """

    if env["game"] == GOPHER_STR:

        # Si nous sommes le premier joueur pour gopher de taille impaire
        # il applique une stétégie optimale
        if env["hex_size"] % 2 == 1 and player == 1:
            return strategy_gopher_opt_impaire(env, state, player)
        # Si on joue à gopher sur taille paire et/ou en tant que joueur 2,
        # on applique notre stratégie globale
        return strategy_gopher(env, state, player, time_left)

    if env["game"] == DODO_STR:
        return strategy_dodo(env, state, player, time_left)

    return (env, (0, 0))


def final_result(state: State, score: Score, player: Player):
    """
    Cette fonction est appelee à la fin de la partie pour afficher le joueur gagnant
    """
    print(f"Ending: {player} wins")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
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
