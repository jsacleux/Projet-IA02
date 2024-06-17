from basic_types import Environment, State, Action, Player, Time, Cell, Strategy
from matrice import getadjacenthex, coordHextoMatrice, creermatrice, set_matrice_to_state, afficher_matrice
from typing import List
from random import randint
import ast

def gopherlegals(env : Environment, state: State, player: Player) -> tuple[list[Cell], list[Cell]]:
    dictionnaire = {}
    ennemi = 0
    sizeGrid = env["hex_size"]
    matrice = env["matrice_bordures"] #une matrice de la taille du plateau, avec seulement les bordures en -1
    if player == 1:
        ennemi = 2
    if player == 2:
        ennemi = 1

    for i in state:
        if i[1] == ennemi:
           for j in getadjacenthex(i[0]):
               (a, b) = coordHextoMatrice(j, sizeGrid)
               val = 0
               for k in state :
                   if k[0] == j :
                       val = k[1]
                       break
                if (matrice[a][b] != -1 and val != 1 and val != 2 and (not (j in dictionnaire))):
                    dictionnaire[j] = "P"
        elif i[1] == player:
            for j in getadjacenthex(i[0]):
                (a, b) = coordHextoMatrice(j, sizeGrid)
                if (matrice[a][b] != -1):
                    dictionnaire[j] = "B"
    cles_p = []  # les coordonés des cases sur lesquelles le joueur peut jouer
    for cle in dictionnaire:
        if dictionnaire[cle] == "P":
            cles_p.append(cle)
    return cles_p

def play_no_verif(state :State, action : Action, player :Player):
    x = []
    for i in state :
        if i[0] == action:
            x.append((action,player))
        else :
            x.append(i)
    return x


def get_next_moves(env :Environment, state : State, player : Player) -> (list[State],list[Action]):
    x = gopherlegals(env,state,player)
    nextmoves = []
    for i in x:
        nextmoves.append(play_no_verif(state,i,player))
    return (nextmoves,x)


def change_player(player : Player) -> int:
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else :
        return 0
    
def has_won(env :Environnement, state : State, player :Player) -> bool:
    x = gopherlegals(env, state, change_player(player))
    if x == []:
        return True
    return False

def getBestNextMove(env : Environment, current_state : State, current_player : Player):
    
    numberOfSimulations = env["n_simulations"]
    boardSize = env["hex_size"]
    
    evaluations = {}
    
    #accumulates scores for each moves
    for generation in range(numberOfSimulations):
        
        player = current_player
        
        boardCopy = current_state
        
        simulationMoves = []
        nextMoves = get_next_moves(boardCopy, player)
        
        score = boardSize * boardSize
        
        while nextMoves != []:
            roll = randint(1, len(nextMoves)) - 1
            boardCopy = nextMoves[roll]
            
            simulationMoves.append(boardCopy)
            
            if has_won(boardCopy, player):
                break
            
            score -= 1
            
            player = change_player(player)
            nextMoves = get_next_moves(boardCopy, player)
        
        firstMove = simulationMoves[0]
        lastMove = simulationMoves[-1]
        
        firstMoveKey = repr(firstMove)
        
        if player == env["us"] and has_won(boardCopy, player):
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




def strategy_gopher_MCTS(env: Environment, state: State, player: Player, time_left: Time) -> tuple[
    Environment, Action]:
    if env["NumérodeTour"] == 0:
        env["NumérodeTour"] += 1
        return (env, ((1, 1), player))
    coup = getBestNextMove(env,state,player)
    print(coup)
    env["NumérodeTour"] += 1
    return (env, (coup, player))