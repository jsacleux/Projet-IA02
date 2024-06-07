from basic_types import Environment, State, Action, Player, Time, Cell
from matrice import getadjacenthex, coordHextoMatrice, creermatrice, set_matrice_to_state
from typing import List
from random import randint



def play_gopher(matrice, coup, joueur):   #(grid: State, player: Player, action: Action) -> State :
    '''Cette fonction retourne l'état de jeu après l'action d'un joueur,'''
    # On utilise ici les coordonnés -(n-1) // n-1
    sizeGrid = int((len(matrice) + 1) / 2)
    (x,y) = coordHextoMatrice((coup[0],coup[1]), sizeGrid)
    print(x,y, " ", coup[0],coup[1]) # affichage du coup joué
    valeur = matrice[x][y]
    if  valeur!= -1 and valeur!= 1 and valeur != 2:
        matrice[x][y] = joueur
    elif valeur == -1 :
        print("coup hors du plateau")
    else :
        print("case déjà occupé")
    return 0

def alpha_beta_gopher(
    grid: State, player: Player, alpha: float, beta: float, depth: int = 0
) -> tuple[float, Action]:
    """explore possibilities"""

    player1: Player = 1
    player2: Player = 2
    best: tuple[float, Action]
    b : float = beta
    a : float = alpha

    if depth == 0 or final(grid):
        return (score_gopher(grid, player1), (-1, -1))

    if player == 1:  # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in gopherlegals(grid):
            tmp = play_gopher(grid, player, item)
            returned_values = alpha_beta_gopher(tmp, player2, a, b, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            a = max(a, best[0])
            if a >= b:
                break
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in gopherlegals(grid):
            tmp = play_gopher(grid, player, item)
            returned_values = alpha_beta_gopher(tmp, player1, a, b, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            b = min(b, best[0])
            if a >= b:
                break
        return best

    raise ValueError("erreur pas de joeur connu")



def strategy_Gopher(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    
    """strategy with alpha evaluation"""
    choice: Action = alpha_beta_gopher(state, player, float("-inf"), float("inf"), env["depth"])[1]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice

def strategy_Gopher_optimale(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    
    return 

def strategy_gopher_random(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    a = set_matrice_to_state(creermatrice(env["hex_size"]), state)
    liste_coups_possibles = gopherlegals(a,state,player)[1]
    print(liste_coups_possibles)
    x = randint(0,len(liste_coups_possibles))
    print(x)
    return (env,(liste_coups_possibles[x],player))


def gopherlegals(matrice, state:State, player:Player) -> tuple[list[Cell],list[Cell]]:
    dictionnaire = {}
    ennemi = 0
    sizeGrid = int((len(matrice) + 1) / 2)
    if player == 1:
        ennemi = 2
    if player == 2:
        ennemi = 1

    for i in state:
        if i[1] == ennemi :
            for j in getadjacenthex(i[0]):
                (a,b) = coordHextoMatrice(j,sizeGrid)
                if (matrice[a][b]!= -1 and matrice[a][b]!= 1 and matrice[a][b]!= 2 and ( not (j in dictionnaire))):
                    dictionnaire[j] = "P"
        elif i[1] == player :
            for j in getadjacenthex(i[0]):
                (a, b) = coordHextoMatrice(j, sizeGrid)
                if (matrice[a][b]!= -1):
                    dictionnaire[j] = "B"
    cles_p = [] # les coordonés des cases sur lesquelles le joueur peut jouer
    cles_b = [] # les coordonés des cases sur lesquelles le joueur ne peut pas jouer
    for cle in dictionnaire:
        if dictionnaire[cle] == "P":
            cles_p.append(cle)
        elif dictionnaire[cle] == "B":
            cles_b.append(cle)
    return (cles_b, cles_p)


def evaluation_function(matrice, state:State, player:Player, env:Environment) -> int :
    cases_bloquees, cases_dispos = gopherlegals(matrice, state, player)
    score = 0
    for case in cases_dispos :
        score += env["pondérations"][case]
    for case in cases_bloquees :
        score -= env["pondérations"][case]
    return score

def final(grid: State) -> bool:
    ''' Cette fonction renvoie vrai si le joueur actuel n'a plus de coups possibles'''
    return 0

def score_gopher(grid: State) -> float : 
    '''Cette fonction renvoie le score du jeu en fonction d'un état final donné'''
    return 0
