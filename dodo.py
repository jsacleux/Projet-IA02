from commons import Environment, State, Action, Player, Strategy, Score, Time



def strategy_Dodo(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    

    if player == 1 : #Maximising player 
        k = 2
    elif player == 2: #Minimising Player
        k = 1

    t = legals_dodo(state)
    if t == [] :
        return score_dodo(state), ((-1,-1),(-1,-1))
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

def legals_dodo(grid: State, player: Player) -> list[Action] :
    '''Cette fonction renvoie l'ensemble des actions possibles pour un joueur'''
    # Cases actuelles +(0,1) ou +(1,1) ou +(1,0) si elle cette case est vide
    return 0

def evaluation_function(grid : State) -> int :
    # Attribuer des pondérations aux cases 
    # Evaluer un score en fonction des cases disponibles et des cases bloquées
    # Les cases en exterieur valent plus que celles au milieu
    return 0

def final(grid: State) -> bool:
    ''' Cette fonction renvoie vrai si il s'agit d'un état final. C'est à dire si le joueur actuel n'a plus de coups possibles'''
    return 0

def score_dodo(grid: State) -> float : 
    '''Cette fonction renvoie le score du jeu en fonction d'un état final donné'''
    return 0