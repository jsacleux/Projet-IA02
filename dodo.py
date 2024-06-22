"""
Ce fichier contient toutes les fonctions permettant de jouer à dodo
"""

import random
import ast

from gndclient import Env, State, Player, Cell, Time, ActionDodo


def get_adjacent_with_direction(
    env: dict, cell: tuple[int, int], player: Player
) -> list[tuple[int, int]]:
    """Cette fonction renvoie la liste des cellules adjacentes à une cellule donnée"""
    x, y = cell
    board_size = env["hex_size"]

    # Trouver les cellules voisines
    if player == 1:
        adjacent = [(x + dx, y + dy) for dx, dy in [(1, 0), (0, 1), (1, 1)]]
    elif player == 2:
        adjacent = [(x + dx, y + dy) for dx, dy in [(-1, 0), (0, -1), (-1, -1)]]

    # Filtrer les cellules en dehors des limites de la grille hexagonale
    adjacent = [
        (i, j)
        for i, j in adjacent
        if -board_size < i < board_size
        and -board_size < j < board_size
        and abs(i - j) < board_size
    ]

    return adjacent


def is_cell_empty(state: State, cell: Cell) -> bool:
    """Cette fonction vérifie si une cellule est vide dans un état de jeu donné."""
    return any(k[0] == cell and k[1] == 0 for k in state)


def get_possible_moves(
    env: Env, state: State, player: Player, cell: Cell
) -> list[tuple[Cell, Cell]]:
    """Cette fonction renvoie la liste des les mouvements possibles pour une cellule donnée."""

    # Déterminer les cases accessibles depuis une certaine case
    adjacent_cells = get_adjacent_with_direction(env, cell, player)

    # Ne conserver que celles qui sont vides
    possible_moves = []
    for adj in adjacent_cells:
        if is_cell_empty(state, adj):
            possible_moves.append((cell, adj))
    return possible_moves


def dodolegals(env: Env, state: State, player: Player) -> list[tuple[Cell, Cell]]:
    """Cette fonction renvoie les actions possibles pour un joueur donné dans un état donné."""
    possible_moves = []
    for cell, owner in state:
        if owner == player:
            possible_moves.extend(get_possible_moves(env, state, player, cell))
    return possible_moves


def play(state: State, action: ActionDodo, player: Player) -> State:
    """Cette fonction renvoie l'état du jeu après une certaine action"""

    cellule_depart, cellule_arrivee = action

    # Création d'un nouvel état de jeu
    new_state = []
    for cellule, couleur in state:

        # Mettre la cellule de depart à 0
        if cellule == cellule_depart:
            new_state.append((cellule_depart, 0))

        # Mettre la cellule d'arrivée depart à 0
        elif cellule == cellule_arrivee:
            new_state.append((cellule_arrivee, player))

        # Garder les autres cellules intactes
        else:
            new_state.append((cellule, couleur))
    return new_state


def get_next_moves(
    env: Env, state: State, player: Player
) -> tuple[list[State], list[ActionDodo]]:
    """
    Cette fonction renvoie
    - la liste des états du jeu après chaque action possible,
    - liste des actions correspondantes
    """

    # Déterminer les coups possibles
    possible_actions = dodolegals(env, state, player)

    # Déterminer l'état de jeu après ces actions
    state_after_each_possible_action = []
    for coup in possible_actions:
        state_after_each_possible_action.append(play(state, coup, player))

    return state_after_each_possible_action, possible_actions


def change_player(player: Player) -> int:
    """Cette fonction change le joueur courant"""
    if player == 1:
        return 2
    if player == 2:
        return 1
    return 0


def has_lost(env: Env, state: State, player: Player) -> bool:
    """
    Cette fonction renvoie vrai si le joueur a perdu
    c'est à dire que le prochain joueur n'a pas de coup possible
    """
    possible_actions_for_next_player = dodolegals(env, state, change_player(player))

    if not possible_actions_for_next_player:
        return True

    return False


def simulate_game(
    env: Env, initial_state: State, initial_player: Player
) -> tuple[ActionDodo, int]:
    """
    Cette fonction simule une partie en jouant des coups aléatoires jusqu'à ce qu'un joueur perde.
    Elle renvoie le premier coup joué dans cette simulation et le score associé à cette simulation.
    """

    # Initialisation des variables
    player = initial_player
    board_copy = initial_state
    score = env["hex_size"] * env["hex_size"]
    simulation_moves = []

    # Déterminer toutes les actions possibles
    next_states, next_actions = get_next_moves(env, board_copy, player)

    # Tant que la partie n'est pas finie, continuer le jeu
    while next_actions:

        # Choisir une action au hasard parmi les actions possibles
        action = random.choice(next_actions)

        # La jouer
        state = next_states[next_actions.index(action)]

        # La garder en mémoire
        simulation_moves.append((action, state))

        if has_lost(env, state, player):
            # Si nous avons perdu, on a un score negatif
            if player == env["us"]:
                score = -env["hex_size"] * env["hex_size"]
            # Si nous avons gagné, on a un score positif
            else:
                score = env["hex_size"] * env["hex_size"]
            # La partir est finie, on peut retourner le score associé au premier coup
            break

        # Si la partie n'est pas finie, continuer le while
        score -= 1
        player = change_player(player)
        next_states, next_actions = get_next_moves(env, state, player)

    # Retourner la premiere action et le score associé
    return simulation_moves[0][0], score


def get_best_next_move(
    env: Env,
    current_state: State,
    current_player: Player,
) -> tuple[Cell, Cell]:
    """
    Cette fonciton détermine le meilleur prochain coup
    en simulant plusieurs parties à partir de l'état actuel.
    """

    evaluations: dict[str, int] = {}

    # Simule des parties et met à jour le score pour chaque première action
    for _ in range(env["n_simulations"]):
        first_move, score = simulate_game(env, current_state, current_player)

        first_move_key = repr(first_move)

        if first_move_key in evaluations:
            evaluations[first_move_key] += score
        else:
            evaluations[first_move_key] = score

    # Trouve l'action avec le meilleur score
    highest_score = float("-inf")
    for move, score in evaluations.items():
        if score > highest_score:
            highest_score = score
            best_move = ast.literal_eval(move)

    return best_move


def strategy_dodo_mcts(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, ActionDodo]:
    """Cette fonction renvoie au serveur l'environnement et l'action à jouer"""

    print("Time remaining ", time_left)

    # Stratégie de monte carlo simple
    coup = get_best_next_move(env, state, player)

    print(f"Coup joueur {player} : {coup}")

    return (env, coup)


def play_randomly_dodo(
    env: Env,
    state: State,
    player: Player,
) -> tuple[Env, ActionDodo]:
    """Cette fonction renvoie une action au hasard"""
    return env, random.choice(dodolegals(env, state, player))
