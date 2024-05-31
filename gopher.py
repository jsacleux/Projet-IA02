from commons import Environment, State, Action, Player, Strategy, Score, Time


def strategy_Gopher(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    

    if player == 1 : #Maximising player 
        k = 2
    elif player == 2: #Minimising Player
        k = 1

    t = legals_gopher(state)
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

def legals_gopher(grid: State, player: Player) -> list[Action] :
    '''Cette fonction renvoie l'ensemble des actions possibles pour un joueur'''
    # Cases adjacentes à ennemi
    # Cases non adjacentes à soi même
    # Legals = intersection des deux
    return 0

def evaluation_function(grid : State) -> int :
    # Attribuer des pondérations aux cases 
    # Evaluer un score en fonction des cases disponibles et des cases bloquées
    # Les cases en exterieur valent plus que celles au milieu
    return 0

def final(grid: State) -> bool:
    ''' Cette fonction renvoie vrai si le joueur actuel n'a plus de coups possibles'''
    return 0

def score_gopher(grid: State) -> float : 
    '''Cette fonction renvoie le score du jeu en fonction d'un état final donné'''
    return 0
