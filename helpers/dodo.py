from basic_types import Environment, State, Action, Player, Time

def play_dodo(matrice, coup, joueur):   #(grid: State, player: Player, action: Action) -> State :
    '''Cette fonction retourne l'état de jeu après l'action d'un joueur,'''
    # On utilise ici les coordonnés -(n-1) // n-1
    sizeGrid = int((len(matrice) + 1) / 2)
    if matrice[coup[0]+sizeGrid-1][coup[1]+sizeGrid-1] != -1:
        matrice[coup[0]+sizeGrid-1][coup[1]+sizeGrid-1] = joueur
    else :
        print("coup hors du plateau")
    return 0


def alpha_beta_dodo(
    grid: State, player: Player, alpha: float, beta: float, depth: int = 0
) -> tuple[float, Action]:
    """explore possibilities"""

    player1: Player = 1
    player2: Player = 2
    best: tuple[float, Action]
    b : float = beta
    a : float = alpha

    if depth == 0 or final(grid):
        return (score_dodo(grid, player1), (-1, -1))

    if player == 1:  # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in legals_dodo(grid):
            tmp = play_dodo(grid, player, item)
            returned_values = alpha_beta_dodo(tmp, player2, a, b, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            a = max(a, best[0])
            if a >= b:
                break
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in legals_dodo(grid):
            tmp = play_dodo(grid, player, item)
            returned_values = alpha_beta_dodo(tmp, player1, a, b, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            b = min(b, best[0])
            if a >= b:
                break
        return best

    raise ValueError("erreur pas de joeur connu")



def strategy_Dodo(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action] :
    
    """strategy with alpha evaluation"""
    choice: Action = alpha_beta_dodo(state, player, float("-inf"), float("inf"), env["depth"])[1]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice




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