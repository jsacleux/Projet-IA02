"""
Ce fichier contient toutes les fonctions permettant de jouer à gopher
"""

import random
import ast

from gndclient import Env, State, Action, Player, Cell, Time, ActionGopher


def premier_tour(state: State) -> bool:
    """ Cette fonction renvoie vrai si il n'y a aucune boule sur la grille"""
    for _, player in state:
        if player != 0:
            return False
    return True


def get_adjacent(env: Env, cell: Cell) -> list[Cell]:
    """ Cette fonction renvoie la liste des cellules adjacentes à une cellule donnée"""
    x, y = cell
    board_size = env["hex_size"]

    # Déplacements pour obtenir les voisins dans une grille axiale
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]

    adjacent = [(x + dx, y + dy) for dx, dy in directions]

    # Filtrer les cellules en dehors des limites de la grille hexagonale
    adjacent = [
        (i, j)
        for i, j in adjacent
        if -board_size < i < board_size
        and -board_size < j < board_size
        and abs(i - j) < board_size
    ]

    return adjacent

def play_randomly(env: Env, state: State, player: Player) -> ActionGopher :
    return random.choice(gopherlegals(env,state,player))

def gopherlegals(env: Env, state: State, player: Player) -> list[Cell]:
    """ Cette fonction renvoie la liste des actions possibles pour un joueur"""

    cases_bloquees = set()
    cases_accessibles = set()

    for cell, color in state:
        if color == player:
            # La case n'est pas vide, on ne peut pas jouer dessus
            cases_bloquees.add(cell)
            # Toutes les cases adjacentes sont bloquées
            cases_bloquees.update(get_adjacent(env, cell))
        elif color == change_player(player):
            # La case est occupee, on ne peut pas jouer dessus
            cases_bloquees.add(cell)
            # Les cases adjacentes sont accessibles ssi elle ne l'étaient pas déjà
            for case_adjacente in get_adjacent(env, cell):
                # Si il existe deja une connexsion ennnemi alors la case est bloquée
                if case_adjacente in cases_accessibles:
                    cases_bloquees.add(case_adjacente)
                # Si pas encore de connexion trouvée alors la case est accessible
                else:
                    cases_accessibles.add(case_adjacente)

    return [case for case in cases_accessibles if case not in cases_bloquees]


def play(state: State, action: ActionGopher, player: Player) -> State:
    """ Cette fonction renvoie l'état du jeu après une certaine action"""
    new_state = []
    for cellule, played_by in state:
        if cellule == action:
            new_state.append((action, player))
        else:
            new_state.append((cellule, played_by))
    return new_state


def get_next_moves(
    env: Env, state: State, player: Player
) -> tuple[list[State], list[ActionGopher]]:
    """ Cette fonction renvoie la liste des états du jeu après chaque action 
    possible, et une liste avec les actions correspondantes"""
    coups_possibles = gopherlegals(env, state, player)
    state_apres_chaque_coup_possible = []

    for coup in coups_possibles:
        state_apres_chaque_coup_possible.append(play(state, coup, player))

    return state_apres_chaque_coup_possible, coups_possibles


def change_player(player: Player) -> int:
    """ Cette fonction change le joueur courant"""
    if player == 1:
        return 2
    if player == 2:
        return 1
    return 0


def has_won(env: Env, state: State, player: Player) -> bool:
    """ Cette fonction renvoie vrai si le joueur a gagné"""
    coups_possibles_adversaire = gopherlegals(env, state, change_player(player))
    if coups_possibles_adversaire == []:
        return True
    return False


def simulate_game(
    env: Env, initial_state: State, initial_player: Player
) -> tuple[Action, int]:
    """ Cette fonction renvoie le score esperé pour chaque action possible"""

    player = initial_player
    board_copy = initial_state
    simulation_moves = []

    next_states, next_actions = get_next_moves(env, board_copy, player)
    score = env["hex_size"] * env["hex_size"]

    while next_actions:
        action = random.choice(next_actions)
        state = next_states[next_actions.index(action)]

        simulation_moves.append((action, state))

        if has_won(env, state, player):
            if player == env["us"]:
                score = env["hex_size"] * env["hex_size"]
            else:
                score = -env["hex_size"] * env["hex_size"]
            break

        score -= 1
        player = change_player(player)
        next_states, next_actions = get_next_moves(env, state, player)

    return simulation_moves[0][0], score

def get_best_next_move(
    env: Env, current_state: State, current_player: Player,
) -> Cell:
    """ Cette fonction renvoie l'action avec le meilleur score'"""
    evaluations: dict[str, int] = {}

    for _ in range(env["n_simulations"]):
        first_move, score = simulate_game(env, current_state, current_player)

        first_move_key = repr(first_move)

        if first_move_key in evaluations:
            evaluations[first_move_key] += score
        else:
            evaluations[first_move_key] = score

    highest_score = float("-inf")
    best_move = None

    for move, score in evaluations.items():
        if score > highest_score:
            highest_score = score
            best_move = ast.literal_eval(move)

    return best_move


def strategy_gopher_mcts(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Cette fonction renvoie au serveur l'environnement et l'action à jouer"""
    print("Time remaining ", time_left)
    if env["premier_tour"] is True:
        print("c'est le premier coup")
        env["premier_tour"] = False
        coup = (0, 0)
        return env, coup
    coup = get_best_next_move(env, state, player)
    print(f"Coup joueur {player} : {coup}")
    return env, coup




def strategy_gopher_opt_impaire(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    # on part du principe que player = 1
    """ Cette fonction est la strategie optimisée pour les grilles impaires """
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

def get_coup_strat_opti(env : Env, state : State, player : Player) -> Action:

    x = set(env["Old_state"])
    y = set(state)
    dernier_coup = y - x

    adjacents_z = get_adjacent(dernier_coup[0])

    coup_origine = (0, 0)

    for case_adjacente in adjacents_z:
        for case_state in state:
            if case_state[0] == case_adjacente:
                coup_origine = case_state[0]

    direction_new_coup = (dernier_coup[0] - coup_origine[0], dernier_coup[1] - coup_origine[1])

    new_coup = (direction_new_coup[0] + coup_origine[0], direction_new_coup[1] + coup_origine[1])

    return new_coup
