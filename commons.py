from typing import Callable, Union
import ast

# Types de base utilisés par l'arbitre
Environment = ... # Ensemble des données utiles (cache, état de jeu...) pour
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
               hex_size: int, total_time: Time) -> Environment :
    '''Cette fonction est lancée au début du jeu. 
    Elle dit à quel jeu on joue, le joueur que l'on est et renvoie l'environnement, 
    c'est-à-dire la structure de donnée (objet, dictionnaire, etc.) que vous utiliserez pour jouer.
    '''
    return 0

def strategy(env: Environment, state: State, player: Player,
             time_left: Time) -> tuple[Environment, Action] :
    '''
    Cette fonction est la strategie que vous utilisez pour jouer. 
    Cette fonction est lancée à chaque fois que c'est à votre joueur de jouer.
    '''
    # Alpha beta en profondeur limitée
    return 0

def final_result(state: State, score: Score, player: Player):
    '''Cette fonction est appelée à la fin du jeu et revoie le joueur gagnant, l'état final et le score.'''
    return 0


# Foncitons de base
def pprint(grid: State) :
    '''Cette fonction affiche la grille à un état donné'''
    return 0

def play(grid: State, player: Player, action: Action) -> State :
    '''Cette fonction retourne l'état de jeu après l'action d'un joueur,'''
    return 0