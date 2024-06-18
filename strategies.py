from typing import Dict, Any
from gndclient import Action, Player, State, Time

Environment = Dict[str, Any]


def strategy_gopher_optimale(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print("New state ", state)
    print("Time remaining ", time_left)

    # TO DO

    return (env, action)


def strategy_gopher(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print("New state ", state)
    print("Time remaining ", time_left)

    # TO DO

    return (env, action)


def strategy_dodo(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print("New state ", state)
    print("Time remaining ", time_left)

    # TO DO

    return (env, action)
