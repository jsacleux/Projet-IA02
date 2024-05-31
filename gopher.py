from commons import Environment, State, Action, Player, Strategy, Score, Time


def strategy_Gopher(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    

    if player == 1 : #Maximising player 
        k = 2
    elif player == 2: #Minimising Player
        k = 1

    t = gopherlegals(state)[1]
    if t == [] :
        return score_gopher(state), (-1,-1)
    
    t2 = [play(state,player,action) for action in t]
    t3 = []
    
    for i in t2:
        t3.append(alphabeta(i, -10, 10, k))
    
    if player == 1 :
        n = dernierIndiceMaximum(t3)
        return (t3[n],t[n])
    if player == 2 :
        n = dernierIndiceMinimum(t3)
        return (t3[n],t[n])
    
    return 

def strategy_Gopher_optimale(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    
    return 

def gopherlegals(matrice, state:State, player:Player) -> [list[Action], list[Action]]: # retourne en première liste les coordonés des cases bloqués pour le joueur, et en deuxième liste les coordonnés des cases sur lesquelles il peut jouer
    dictionnaire = {}

    ennemi = 0
    if player == 1:
        ennemi = 2
    if player == 2:
        ennemi = 1
    
    for i in state:
        if i[1] == ennemi :
            for j in getadjacent(i[0]) :
                if (matrice[j[0]][j[1]]!= -1 and matrice[j[0]][j[1]]!= 1 and matrice[j[0]][j[1]]!= 2 and dictionnaire[j]!= "B"):
                    dictionnaire[j] = "P"
        if i[1] == player :
            for j in getadjacent(i[0]) :
                if (matrice[j[0]][j[1]]!= -1):
                    dictionnaire[j] = "B"
    cles_p = [] # les coordonés des cases sur lesquelles le joueur peut jouer
    cles_b = [] # les coordonés des cases sur lesquelles le joueur ne peut pas jouer
    for cle in dictionnaire:
        if dictionnaire[cle] == "P":
            cles_p.append(cle)
        elif dictionnaire[cle] == "B":
            cles_b.append(cle)
    return [cles_b, cles_p]

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
