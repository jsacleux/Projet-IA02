from gndclient import Env, State, Action, Player, Cell, Time
from random import randint
import ast

def premier_tour(state : State) -> bool :
    for cell, player in state:
        if player != 0:
            return False
    return True

def get_adjacent(env: Env, cell: Cell) -> list[Cell]:
    x, y = cell
    boardSize = env["hex_size"]

    # Déplacements pour obtenir les voisins dans une grille axiale
    directions = [
        (1, 0), (-1, 0), 
        (0, 1), (0, -1), 
        (1, 1), (-1, -1)
    ]

    adjacent = [(x + dx, y + dy) for dx, dy in directions]

    # Filtrer les cellules en dehors des limites de la grille hexagonale
    adjacent = [
        (i, j) for i, j in adjacent
        if -boardSize < i < boardSize and -boardSize < j < boardSize
        and abs(i - j) < boardSize  
    ]

    return adjacent

def gopherlegals(env: Env, state: State, player: Player) -> list[Cell]:
    
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
            #Les cases adjacentes sont accessibles ssi elle ne l'étaient pas déjà
            for case_adjacente in get_adjacent(env, cell):
                #Si il existe deja une connexsion ennnemi alors la case est bloquée
                if case_adjacente in cases_accessibles :
                    cases_bloquees.add(case_adjacente)
                #Si pas encore de connexion trouvée alors la case est accessible
                else :
                    cases_accessibles.add(case_adjacente)

    return [ case for case in cases_accessibles if case not in cases_bloquees]


def play_no_verif(state: State, action: Action, player: Player) -> State:
    
    new_state = []
    for cellule, played_by in state:
        if cellule == action:
            new_state.append((action, player))
        else:
            new_state.append((cellule, played_by))
    return new_state


def get_next_moves(
    env: Env, state: State, player: Player
) -> tuple[list[State], list[Action]]:
    
    coups_possibles = gopherlegals(env, state, player)
    state_apres_chaque_coup_possible = []

    for coup in coups_possibles:
        state_apres_chaque_coup_possible.append(play_no_verif(state, coup, player))

    return state_apres_chaque_coup_possible, coups_possibles

def change_player(player: Player) -> int:
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        return 0


def has_won(env: Env, state: State, player: Player) -> bool:
    coups_possibles_adversaire = gopherlegals(env, state, change_player(player))
    if coups_possibles_adversaire == []:
        return True
    return False


def getBestNextMove(env: Env, current_state: State, current_player: Player, time: Time) -> Cell:

    numberOfSimulations = env["n_simulations"]
    boardSize = env["hex_size"]

    evaluations = {}

    # accumulates scores for each moves
    for generation in range(numberOfSimulations):

        player = current_player

        boardCopy = current_state

        simulationMoves = []
        next_states, next_actions = get_next_moves(env, boardCopy, player)
        
        score = boardSize * boardSize

        while next_actions != []:
            
            roll = randint(0, len(next_actions)) - 1
            action = next_actions[roll]
            state = next_states[roll]

            simulationMoves.append((action, state))

            if has_won(env, state, player):
                break

            score -= 1

            player = change_player(player)
            next_states, next_actions = get_next_moves(env, state, player)

        tuple_first_move = simulationMoves[0]
        tuple_last_move = simulationMoves[-1]

        firstMoveKey = repr(tuple_first_move[0])

        if player == env["us"] and has_won(env, state, player):
            score *= -1

        if firstMoveKey in evaluations:
            evaluations[firstMoveKey] += score
        else:
            evaluations[firstMoveKey] = score

    bestMove = []
    highestScore = 0
    firstRound = True

    for move, score in evaluations.items():
        if firstRound or score > highestScore:
            highestScore = score
            bestMove = ast.literal_eval(move)
            firstRound = False

    return bestMove


def strategy_gopher_MCTS(
    env: Env, state: State, player: Player, time_left: Time
) -> tuple[Env, Action]:
    
    if env["premier_tour"] == True :
        print("c'est le premier coup")
        env["premier_tour"] = False
        coup = (0,0)
        return env, coup
    coup = getBestNextMove(env, state, player, time_left)
    print(coup)
    return env, coup
