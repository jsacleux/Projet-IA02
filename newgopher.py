from gndclient import Env, State, Action, Player, Cell, Time
from matrice import getadjacenthex, coordHextoMatrice
from random import randint
import ast

def premier_tour(state : State) -> bool :
    for cell, player in state:
        if player != 0:
            return False
    return True

def gopherlegals_bis(env: Env, state: State, player: Player) -> list[Cell]:
    # TO DO : debug
    dictionnaire = {}
    ennemi = 0
    sizeGrid = env["hex_size"]
    matrice = env[
        "matrice_bordures"
    ]  # une matrice de la taille du plateau, avec seulement les bordures en -1
    if player == 1:
        ennemi = 2
    if player == 2:
        ennemi = 1
    
    for i in state:
        if i[1] == ennemi:
            for j in getadjacenthex(i[0]):
                (a, b) = coordHextoMatrice(j, sizeGrid)
                val = 0
                for k in state:
                    if k[0] == j:
                        val = k[1]
                        break
                if (
                    matrice[a][b] != -1
                    and val != 1
                    and val != 2
                    and (not (j in dictionnaire))
                ):
                    dictionnaire[j] = "P"
        elif i[1] == player:
            for j in getadjacenthex(i[0]):
                (a, b) = coordHextoMatrice(j, sizeGrid)
                if matrice[a][b] != -1:
                    dictionnaire[j] = "B"
    cles_p = []  # les coordonés des cases sur lesquelles le joueur peut jouer
    for cle in dictionnaire:
        if dictionnaire[cle] == "P":
            cles_p.append(cle)
    return cles_p


# TO DO : refactor parce que c'est chat gpt
def get_adjacent(env: dict, cell: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = cell
    boardSize = env["hex_size"]

    # Déplacements pour obtenir les voisins dans une grille axiale
    directions = [
        (1, 0), (-1, 0), 
        (0, 1), (0, -1), 
        (1, 1), (-1, -1)
    ]

    adjacent = [(x + dx, y + dy) for dx, dy in directions]
    #print("adjacentes à priori", adjacent)

    # Filtrer les cellules en dehors des limites de la grille hexagonale
    adjacent = [
        (i, j) for i, j in adjacent
        if -boardSize < i < boardSize and -boardSize < j < boardSize
        and abs(i - j) < boardSize  # Assurer que (i, j) reste dans le losange
    ]
    #print("adjacentes à posteriori", adjacent)
    return adjacent

def gopherlegals(env: Env, state: State, player: Player) -> list[Cell]:
    
    cases_bloquees = set()
    cases_accessibles = set()

    #print("state:", state)
    for cell, color in state:
        if color == player:
            cases_bloquees.add(cell) # La case n'est pas vide, on ne peut pas jouer dessus
            cases_bloquees.update(get_adjacent(env, cell)) # Les cases sont adjacentes à nous meme, on ne peut pas jouer dessus
        elif color == change_player(player):
            cases_bloquees.add(cell) # La case est occupee, on ne peut pas jouer dessus
            cases_accessibles.update(get_adjacent(env, cell)) # Les cases sont adjacentes à l'ennemi, on peut jouer dessus

    #print("cases_accessibles:", cases_accessibles)
    #print("cases_bloquees:", cases_bloquees)
    return list(cases_accessibles - cases_bloquees)


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
    
    coups_possibles = gopherlegals_bis(env, state, player)
    #print('legals :', coups_possibles)
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
    x = gopherlegals_bis(env, state, change_player(player))
    if x == []:
        return True
    return False


def getBestNextMove(env: Env, current_state: State, current_player: Player, time: Time):

    numberOfSimulations = env["n_simulations"]
    boardSize = env["hex_size"]

    evaluations = {}

    # accumulates scores for each moves
    for generation in range(numberOfSimulations):

        player = current_player

        boardCopy = current_state

        simulationMoves = []
        next_states, next_actions = get_next_moves(env, boardCopy, player)
        #print('Actions possibles premier coup', next_actions)
        
        score = boardSize * boardSize

        while next_actions != []:
            
            #print('Actions possibles', next_actions)
            roll = randint(0, len(next_actions)) - 1
            action = next_actions[roll]
            state = next_states[roll]
            print('Action choisie',action)
            #print('State', state)

            simulationMoves.append((action, state))

            if has_won(env, state, player):
                break

            score -= 1

            player = change_player(player)
            next_states, next_actions = get_next_moves(env, state, player)
            #print('Nouvelles actions possibles', next_actions)

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
        env["premier_tour"] = False
        return (env, (1, 1))
    coup = getBestNextMove(env, state, player, time_left)
    print(coup)
    return (env, coup)
