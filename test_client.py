#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR

from strategies import strategy_dodo, strategy_gopher, strategy_gopher_optimale
from gopher import premier_tour, strategy_gopher_MCTS
from dodo import strategy_dodo_MCTS

Environment = Dict[str, Any]


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:

    print("Init")
    print(
        f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )

    x = {}
    x["game"] = game
    x["hex_size"] = hex_size
    x["us"] = player
    x["premier_tour"] = premier_tour(state)
    x["n_simulations"] = 50
    return x


def strategy_brain(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print("New state ", state)
    print("Time remaining ", time_left)
    print("What's your play ? ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)
    return (env, t)


def strategy(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Cette fonction est la strategie que vous utilisez pour jouer.
    Cette fonction est lancée à chaque fois que c'est à votre joueur de jouer.
    """
    if env["game"] == GOPHER_STR:
        if env["hex_size"] % 2 == 1 and player == 2:
            return strategy_gopher_optimale(env, state, player, time_left)
        return strategy_gopher(env, state, player, time_left)
    if env["game"] == DODO_STR:
        return strategy_dodo(env, state, player, time_left)

def strategy_provisoire(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    MCTS dodo et gopher
    """
    if env["game"] == GOPHER_STR:
        return strategy_gopher_MCTS(env, state, player, time_left)
    if env["game"] == DODO_STR:
        return strategy_dodo_MCTS(env, state, player, time_left)

def final_result(state: State, score: Score, player: Player):
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
        strategy_provisoire,
        final_result,
        gui=True,
    )
