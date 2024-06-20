"""
Ce fichier contient toutes les fonctions permettant de jouer à dodo
"""

import random
import ast

from gndclient import Env, State, Action, Player, Cell, Time, ActionDodo

def get_adjacent(
    env: dict, cell: tuple[int, int], player: Player
) -> list[tuple[int, int]]:
    """ Cette fonction renvoie la liste des cellules adjacentes à une cellule donnée"""
    x, y = cell
    board_size = env["hex_size"]

    # Déplacements pour obtenir les voisins dans une grille axiale
    directionsrouge = [(1, 0), (0, 1), (1, 1)]

    directionsbleu = [(-1, 0), (0, -1), (-1, -1)]
    if player == 1:
        adjacent = [(x + dx, y + dy) for dx, dy in directionsrouge]
    elif player == 2:
        adjacent = [(x + dx, y + dy) for dx, dy in directionsbleu]
    # Filtrer les cellules en dehors des limites de la grille hexagonale
    adjacent = [
        (i, j)
        for i, j in adjacent
        if -board_size < i < board_size
        and -board_size < j < board_size
        and abs(i - j) < board_size  # Assurer que (i, j) reste dans le losange
    ]
    return adjacent

def is_cell_empty(state: State, cell: Cell) -> bool:
    """Vérifie si la cellule est vide dans l'état donné."""
    return any(k[0] == cell and k[1] == 0 for k in state)

def get_possible_moves(
    env: Env, state: State, player: Player, cell: Cell
) -> list[tuple[Cell, Cell]]:
    """Trouve les mouvements possibles pour une cellule donnée."""
    possible_moves = []
    adjacent_cells = get_adjacent(env, cell, player)
    for adj in adjacent_cells:
        if is_cell_empty(state, adj):
            possible_moves.append((cell, adj))
    return possible_moves

def dodolegals(env: Env, state: State, player: Player) -> list[tuple[Cell, Cell]]:
    """Renvoie les actions possibles pour le joueur donné dans l'état donné."""
    possible_moves = []
    for cell, owner in state:
        if owner == player:
            possible_moves.extend(get_possible_moves(env, state, player, cell))
    return possible_moves


def play(state: State, action: ActionDodo, player: Player) -> State:
    """ Cette fonction renvoie l'état du jeu après une certaine action"""
    new_state = []
    for cellule, played_by in state:
        if cellule == action[0]:
            new_state.append((action[0], 0))
        elif cellule == action[1]:
            new_state.append((action[1], player))
        else:
            new_state.append((cellule, played_by))
    return new_state


def get_next_moves(
    env: Env, state: State, player: Player
) -> tuple[list[State], list[ActionDodo]]:
    """ Cette fonction renvoie la liste des états du jeu après chaque action 
    possible, et une liste avec les actions correspondantes"""
    coups_possibles = dodolegals(env, state, player)
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
    coups_possibles_adversaire = dodolegals(env, state, change_player(player))
    if not coups_possibles_adversaire:
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
    """ Cette fonction renvoie l'action avec le meilleur score"""
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



def strategy_dodo_mcts(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    """ Cette fonction renvoie au serveur l'environnement et l'action à jouer"""
    print("Time remaining ", time_left)
    coup = get_best_next_move(env, state, player)
    print(f"Coup joueur {player} : {coup}")
    return (env, coup)


def play_randomly_dodo(
    env: Env, state: State, player: Player, time_left: Time
)-> tuple[Env, Action]:
    """ Cette fonction renvoie une action au hasard"""
    return random.choice(dodolegals(env,state,player))