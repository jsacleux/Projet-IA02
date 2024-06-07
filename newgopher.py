from basic_types import Environment, State, Action, Player, Time, Cell, Strategy
from matrice import getadjacenthex, coordHextoMatrice, creermatrice, set_matrice_to_state, afficher_matrice
from typing import List
from random import randint


def play_gopher(matrice, coup, joueur):  # (grid: State, player: Player, action: Action) -> State :
    sizeGrid = int((len(matrice) + 1) / 2)
    (x, y) = coordHextoMatrice((coup[0], coup[1]), sizeGrid)
    print(x, y, " ", coup[0], coup[1])
    valeur = matrice[x][y]
    if valeur != -1 and valeur != 1 and valeur != 2:
        matrice[x][y] = joueur
    elif valeur == -1:
        print("coup hors du plateau")
    else:
        print("case déjà occupé")
    return 0

def strategy_gopher_random(env: Environment, state: State, player: Player, time_left: Time) -> tuple[
    Environment, Action]:
    if env["NumérodeTour"] == 0:
        env["NumérodeTour"] += 1
        return (env, ((1, 1), player))
    a = set_matrice_to_state(creermatrice(env["hex_size"]), state)
    liste_coups_possibles = gopherlegals(a, state, player)[1]
    if len(liste_coups_possibles) <= 0:
        print('partie perdue par le joueur : ', player)
        return (env, ((0, 0), 3))
    print(liste_coups_possibles)
    x = randint(0, len(liste_coups_possibles) - 1)
    print(x)
    env["NumérodeTour"] += 1
    return (env, (liste_coups_possibles[x], player))


def get_lastmove(oldstate:State, newstate:State):
    setoldstate = set(oldstate)
    setnewstate = set(newstate)
    added_elements = setnewstate - setoldstate
    added_elements = tuple(added_elements)
    return added_elements


def update_environement_moves(env : Environment, newstate: State):
    last_move = get_lastmove(env["lastState"], newstate)
    to_update = getadjacenthex(last_move[0])
    last_joueur = last_move[1]
    for i in to_update:
        if env["gopherJoueur"+last_joueur+"cases"][i] == "B":
            return



    return


def partieGopher(strategieJ1: Strategy, strategieJ2: Strategy, taillegrille: int):
    matriceAffichage = creermatrice(taillegrille)
    enviro = {}
    enviro["game"] = "gopher"
    enviro["hex_size"] = taillegrille
    enviro["lastState"] = []
    enviro["gopherJoueur1cases"] = { }
    enviro["gopherJoueur2cases"] = { }
    enviro["gopherJoueur1casesaccessibles"] = []
    enviro["gopherJoueur2casesaccessibles"] = []
    enviro["NumérodeTour"] = 0

    statecurrentgame = []
    Joueuractif = 1

    print("Coup du joueur ", Joueuractif)
    coupJoueur1 = strategieJ1(enviro, statecurrentgame, 1, 4)[1]
    statecurrentgame.append(coupJoueur1)
    play_gopher(matriceAffichage, coupJoueur1[0], coupJoueur1[1])
    afficher_matrice(matriceAffichage)
    Joueuractif = 2

    while ( len(enviro["gopherJoueur"+Joueuractif+"casesaccessibles"])> 0):
        if Joueuractif == 1:
            print("Coup du joueur ", Joueuractif)
            coupJoueur1 = strategieJ1(enviro, statecurrentgame, 1, 4)[1]
            statecurrentgame.append(coupJoueur1)
            play_gopher(matriceAffichage, coupJoueur1[0], coupJoueur1[1])
            afficher_matrice(matriceAffichage)
            Joueuractif = 2
        elif Joueuractif == 2:
            print("Coup du joueur ", Joueuractif)
            coupJoueur2 = strategieJ2(enviro, statecurrentgame, 2, 4)[1]
            statecurrentgame.append(coupJoueur2)
            play_gopher(matriceAffichage, coupJoueur2[0], coupJoueur2[1])
            afficher_matrice(matriceAffichage)
            Joueuractif = 1
    if len(gopherlegals(matriceAffichage, statecurrentgame, Joueuractif)[1]) == 0:
        if Joueuractif == 1:
            print("Le  Joueur 2 a gagné")
        else:
            print("Le  Joueur 1 a gagné")
    return


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
    cles_b = []  # les coordonés des cases sur lesquelles le joueur ne peut pas jouer
    for cle in dictionnaire:
        if dictionnaire[cle] == "P":
            cles_p.append(cle)
        elif dictionnaire[cle] == "B":
            cles_b.append(cle)
    return (cles_b, cles_p)


