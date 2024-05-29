from commons import State, Action, Player, Strategy, Score

def legals(grid: State, player: Player) -> list[Action] :
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

def score(grid: State) -> float : 
    '''Cette fonction renvoie le score du jeu en fonction d'un état final donné'''
    return 0