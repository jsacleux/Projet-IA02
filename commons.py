from basic_types import State, Player, Time, Environment, Action, Score
from gopher import strategy_Gopher_optimale, strategy_Gopher, play_gopher
from dodo import strategy_Dodo
from matrice import creermatrice, afficher_matrice




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


def test():

    return

if __name__ == '__main__':

    test()

