from typing import Callable
from hexagones import _Hex
import ast

# Structures de données
Grid = _Hex
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[State, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0
BLUE = 1
RED = 2

# Foncitons de base
def pprint(grid: State) :
    '''Cette fonction affiche la grille à un état donné'''
    return 0

def play(grid: State, player: Player, action: Action) -> State :
    '''Cette fonction retourne l'état de jeu après l'action d'un joueur,'''
    return 0

def strategy(grid: State, player: Player) -> Action :
    '''Renvoie l'action choisie par un joueur en fonction de sa stratégie'''
    return 0

def strategy_brain(grid: State, player: Player) -> Action:
    '''Cette fonction créee une interface texte permettant à un humain de jouer.'''
    print("à vous de jouer: ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)

    return t

def strategy_first_legal(grid: State, player: Player) -> Action :
    '''Ce joueur joue toujours la première action légale disponible.'''
    return 0

def strategy_random(grid: State, player: Player) -> Action :
    '''Ce joueur joue au hasard l'une des actions légales disponibles.'''
    return 0

def minmax(grid: State, player: Player) -> float :
    '''Cette fonction renvoie le score optimal de la partie en fonction d'un état'''
    return 0

def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[float, Action]:
    '''Cette fonction renvoie l'action amenant au score optimal de la partie et ce score.'''
    return 0

def strategy_minmax(grid: State, player: Player) -> Action :
    '''Ce joueur joue en maximaisant son score'''
    return 0