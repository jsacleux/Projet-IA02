from basic_types import Environment, State, Action, Player, Time, Cell, Strategy
from matrice import getadjacenthex, coordHextoMatrice, creermatrice, set_matrice_to_state, afficher_matrice
from typing import List
from random import randint

def gopherlegals(matrice, state: State, player: Player) -> tuple[list[Cell], list[Cell]]:
    dictionnaire = {}
    ennemi = 0
    sizeGrid = int((len(matrice) + 1) / 2)
    if player == 1:
        ennemi = 2
    if player == 2:
        ennemi = 1

    for i in state:
        if i[1] == ennemi:
            for j in getadjacenthex(i[0]):
                (a, b) = coordHextoMatrice(j, sizeGrid)
                if (matrice[a][b] != -1 and matrice[a][b] != 1 and matrice[a][b] != 2 and (not (j in dictionnaire))):
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


def get_next_moves(state : State, player : Player) -> list[State]:
    x = gopherlegals(a,state,player)
    nextmoves = []
    for i in x:
        nextmoves.append(play_no_verif(state,i,player))
    return nextmoves


def change_player(player : Player) -> int:
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else :
        return 0
def has_won(state : State, player :Player) -> bool:
    x = gopherlegals(a, state, change_player(player))
    if x == []:
        return True
    return False