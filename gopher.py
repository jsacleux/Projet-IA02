from commons import State, Action, Player, Strategy, Score

def legals(grid: State, player: Player) -> list[Action] :
    '''Cette fonction renvoie l'ensemble des actions possibles pour un joueur'''
    return 0

def final(grid: State) -> bool:
    ''' Cette fonction renvoie vrai si le joueur actuel n'a plus de coups possibles'''
    return 0

def score(grid: State) -> float : 
    '''Cette fonction renvoie le score du jeu en fonction d'un état final donné'''
    return 0

def gopher(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score :
    '''Cette fonction  s'occupe de la boucle de jeu, du gagnant et renvoie le score à la fin du jeu.'''
    return 0