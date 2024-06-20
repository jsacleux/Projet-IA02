import random
import ast

from gndclient import Env, State, Action, Player, Cell, Time, ActionDodo


def premier_tour(state: State) -> bool:
    for _, player in state:
        if player != 0:
            return False
    return True


def get_adjacent(
    env: dict, cell: tuple[int, int], player: Player
) -> list[tuple[int, int]]:
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


def dodolegals(env: Env, state: State, player: Player) -> list[tuple[Cell, Cell]]:
    coup_possibles = []

    for i in state:
        if i[1] == player:
            caseadjacentes = get_adjacent(env, i[0], player)
            for j in caseadjacentes:
                for k in state:
                    if k[0] == j:
                        if k[1] == 0:
                            coup_possibles.append((i[0], j))

    return coup_possibles


def play_no_verif(state: State, action: ActionDodo, player: Player) -> State:
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
    coups_possibles = dodolegals(env, state, player)
    state_apres_chaque_coup_possible = []

    for coup in coups_possibles:
        state_apres_chaque_coup_possible.append(play_no_verif(state, coup, player))

    return state_apres_chaque_coup_possible, coups_possibles


def change_player(player: Player) -> int:
    if player == 1:
        return 2
    if player == 2:
        return 1
    return 0


def has_won(env: Env, state: State, player: Player) -> bool:
    coups_possibles_adversaire = dodolegals(env, state, change_player(player))
    if coups_possibles_adversaire == []:
        return True
    return False


def get_best_next_move(env: Env, current_state: State, current_player: Player, time: Time):

    number_simulations = env["n_simulations"]
    board_size = env["hex_size"]

    evaluations: dict[str, int] = {}

    for _ in range(number_simulations):

        player = current_player
        board_copy = current_state
        simulation_moves = []

        next_states, next_actions = get_next_moves(env, board_copy, player)

        score = board_size * board_size

        while next_actions != []:

            action = random.choice(next_actions)
            state = next_states[next_actions.index(action)]

            simulation_moves.append((action, state))

            if has_won(env, state, player):
                if player == env["us"]:
                    score = board_size * board_size
                else:
                    score = -board_size * board_size
                break

            score -= 1

            player = change_player(player)
            next_states, next_actions = get_next_moves(env, state, player)

        first_move_key = repr(simulation_moves[0][0])

        if first_move_key in evaluations:
            evaluations[first_move_key] += score
        else:
            evaluations[first_move_key] = score

    highest_score = float("-inf")

    for move, score in evaluations.items():
        if score > highest_score:
            highest_score = score
            best_move = ast.literal_eval(move)

    return best_move


def strategy_dodo_mcts(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:

    coup = get_best_next_move(env, state, player, time_left)
    print(f"Coup joueur {player} : {coup}")
    return (env, coup)
