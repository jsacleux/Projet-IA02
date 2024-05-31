from typing import Callable, Union
import ast
from gopher import strategy_Gopher_optimale, strategy_Gopher
from dodo import strategy_Dodo

# Types de base utilisés par l'arbitre
Environment = dict # Ensemble des données utiles (cache, état de jeu...) pour
                  # que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell] # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int # 1 ou 2
State = list[tuple[Cell, Player]] # État du jeu pour la boucle de jeu
Score = int
Time = int


# Fonctions demandées par le prof

def initialize(game: str, state: State, player: Player,
               hex_size: int, total_time: Time) -> Environment:
    
    '''Cette fonction est lancée au début du jeu. 
    Elle dit à quel jeu on joue, le joueur que l'on est et renvoie l'environnement, 
    c'est-à-dire la structure de donnée (objet, dictionnaire, etc.) que vous utiliserez pour jouer.
    '''

    x = {}
    x["game"] = game
    x["hex_size"] = hex_size
    
    # Pas de temps dans environnement mais pris en compte dans stratégie

    # implémenter le cache
    # implémenter la grille de jeu
    # implémenter la pondération de la grille  (Les cases en exterieur valent plus que celles au milieu)

    return x

def strategy(env: Environment, state: State, player: Player,
             time_left: Time) -> tuple[Environment, Action]:
    '''
    Cette fonction est la strategie que vous utilisez pour jouer. 
    Cette fonction est lancée à chaque fois que c'est à votre joueur de jouer.
    '''
    if Environment["game"] == "Gopher":
        if Environment["hex_size"] % 2 == 1 and player == 2:
            return strategy_Gopher_optimale(env, state, player, time_left)
        return strategy_Gopher(env, state, player, time_left)
    if Environment["game"] == "Dodo":
        return strategy_Dodo(env, state, player, time_left)
    return tuple[0,0]
            

def final_result(state: State, score: Score, player: Player):
    '''Cette fonction est appelée à la fin du jeu et revoie le joueur gagnant, l'état final et le score.'''
    # Sert pour faire des stats ou changer notre stratégie
    return 0


# Foncitons de base
def pprint(grid: State) :
    '''Cette fonction affiche la grille à un état donné'''
    return 0

def play(matrice, coup, joueur):   #(grid: State, player: Player, action: Action) -> State :
    '''Cette fonction retourne l'état de jeu après l'action d'un joueur,'''
    # On utilise ici les coordonnés -(n-1) // n-1
    sizeGrid = int((len(matrice) + 1) / 2)
    if matrice[coup[0]+sizeGrid-1][coup[1]+sizeGrid-1] != -1:
        matrice[coup[0]+sizeGrid-1][coup[1]+sizeGrid-1] = joueur
    else :
        print("coup hors du plateau")
    return 0

