"""
Ce fichier contient toutes les fonctions permettant de jouer à gopher
"""

import random
import ast

from gndclient import Env, State, Action, Player, Cell, Time, ActionGopher


def premier_tour(state: State) -> bool:
    """Cette fonction renvoie vrai si il n'y a aucune boule sur la grille"""

    # Si on trouve une case différente de 0, ce n'est pas le premier tour
    for _, player in state:
        if player != 0:
            return False
    return True


def get_adjacent(env: Env, cell: Cell) -> list[Cell]:
    """Cette fonction renvoie la liste des cellules adjacentes à une cellule donnée"""
    x, y = cell
    board_size = env["hex_size"]

    # Trouver les cellules voisines
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


def play_randomly_gopher(env: Env, state: State, player: Player) -> ActionGopher:
    """Cette fonction renvoie une action au hasard"""
    return random.choice(gopherlegals(env, state, player))


def gopherlegals(env: Env, state: State, player: Player) -> list[Cell]:
    """Cette fonction renvoie la liste des actions possibles pour un joueur"""

    # Ensemble des cases accessibles (adjacentes à au moins une boule ennemie)
    cases_bloquees = set()

    # Ensemble des cases bloquées (occupées, adjacentes à une boule amie,
    # adjacente à plus d'une boule ennemie)
    cases_accessibles = set()

    # Parcourir le plateau pour déterminer les cases accessibles et bloquées
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

    # Les cases possibles sont celles qui sont à la fois accessibles ET non bloquées
    return [case for case in cases_accessibles if case not in cases_bloquees]


def play(state: State, action: ActionGopher, player: Player) -> State:
    """Cette fonction renvoie l'état du jeu après une certaine action"""

    # Création d'un nouvel état de jeu
    new_state = []
    for cellule, played_by in state:

        # Ajouter notre boule
        if cellule == action:
            new_state.append((action, player))

        # Garder les autres cellules intactes
        else:
            new_state.append((cellule, played_by))

    return new_state


def get_next_moves(
    env: Env, state: State, player: Player
) -> tuple[list[State], list[ActionGopher]]:
    """
    Cette fonction renvoie la liste des états du jeu après chaque action
    possible, et une liste avec les actions correspondantes
    """

    # Déterminer les coups possibles
    coups_possibles = gopherlegals(env, state, player)

    # Déterminer l'état de jeu après ces actions
    state_apres_chaque_coup_possible = []
    for coup in coups_possibles:
        state_apres_chaque_coup_possible.append(play(state, coup, player))

    return state_apres_chaque_coup_possible, coups_possibles


def change_player(player: Player) -> int:
    """Cette fonction change le joueur courant"""
    if player == 1:
        return 2
    if player == 2:
        return 1
    return 0


def has_won(env: Env, state: State, player: Player) -> bool:
    """
    Cette fonction renvoie vrai si le joueur a gagné,
    c'est à dire que le prochain joueur n'a pas de coup possible
    """

    coups_possibles_adversaire = gopherlegals(env, state, change_player(player))

    if coups_possibles_adversaire == []:
        return True

    return False


def simulate_game(
    env: Env, initial_state: State, initial_player: Player
) -> tuple[Action, int]:
    """
    Cette fonction simule une partie en jouant des coups aléatoires jusqu'à ce qu'un joueur perde.
    Elle renvoie le premier coup joué dans cette simulation et le score associé à cette simulation.
    """

    # Initialisation des variables
    player = initial_player
    board_copy = initial_state
    simulation_moves = []
    score = env["hex_size"] * env["hex_size"]

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

        # Si la partie est finie, renvoyer les score correspondant
        if has_won(env, state, player):
            if player == env["us"]:
                score = score
            else:
                score = -score
            break

        # Sinon continuer la partie
        player = change_player(player)
        next_states, next_actions = get_next_moves(env, state, player)

    # Retourner la premiere action et le score associé
    return simulation_moves[0][0], score


def get_best_next_move(
    env: Env,
    current_state: State,
    current_player: Player,
) -> Cell:
    """Cette fonction renvoie l'action avec le meilleur score'"""

    evaluations: dict[str, int] = {}

    # Simule des parties et met à jour le score pour chaque première action
    for _ in range(env["n_simulations"]):
        first_move, score = simulate_game(env, current_state, current_player)

        first_move_key = repr(first_move)

        if first_move_key in evaluations:
            evaluations[first_move_key] += score
        else:
            evaluations[first_move_key] = score

    highest_score = float("-inf")

    # Trouve l'action avec le meilleur score
    for move, score in evaluations.items():
        if score > highest_score:
            highest_score = score
            best_move = ast.literal_eval(move)

    return best_move


def strategy_gopher_mcts(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, ActionGopher]:
    """
    Cette fonciton détermine le meilleur prochain coup
    en simulant plusieurs parties à partir de l'état actuel.
    """

    print("Time remaining ", time_left)

    # Au premier tour, on décide arbitrairement de jouer en (0,0)
    if env["premier_tour"] is True:
        env["premier_tour"] = False
        coup = (0, 0)
        return env, coup

    # Sinon on utilise monte carlo
    coup = get_best_next_move(env, state, player)
    print(f"Coup joueur {player} : {coup}")
    return env, coup


def get_coup_strat_opti(env: Env, state: State) -> ActionGopher:
    """Cette fonction permet de retourner l'action à jouer dans le cas où nous sommes le player 1,
    et que la grille est de taille impaire."""

    # Récupérer l'état de la grille avant le coup du joueur ennemi
    old_state = env["Old_state"]

    # Déterminer le dernier coup du joueur adverse en comparant l'ancier et le nouvel état de jeu
    x = set(old_state)
    y = set(state)
    set_dernier_coup = y - x
    dernier_coup, _ = next(iter(set_dernier_coup))

    # Trouver la cellule qui a permis à l'ennemi de poser sa boule
    adjacents_to_last_action = get_adjacent(env, dernier_coup)

    for adjacent_cell in adjacents_to_last_action:
        for cell, player in state:
            if cell == adjacent_cell and player != 0:
                coup_origine = cell

    # Calculer la direction du dernier coup
    direction_new_coup = (
        dernier_coup[0] - coup_origine[0],
        dernier_coup[1] - coup_origine[1],
    )

    # Retourner l'action qui permet de suivre cette direction
    new_coup = (
        direction_new_coup[0] + dernier_coup[0],
        direction_new_coup[1] + dernier_coup[1],
    )

    return new_coup
