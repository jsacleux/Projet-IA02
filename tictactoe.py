#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:21:59 2024

@author: ia02p075
"""

from typing import * 
from random import *
import ast

Grid = tuple[tuple[int,int,int],tuple[int,int,int],tuple[int,int,int]]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[Grid, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2



def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    t = [[9,9,9],[9,9,9],[9,9,9]]
    for i in range(len(grid)):
        for j in range(len(grid)):
            t[i][j] = grid[i][j]
    return t
    

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    #test t = tuple((tuple(l) for l in [[1,2,3],[4,5,6],[7,8,9]]))
    t = tuple((tuple(l) for l in grid))
    return t


def line(grid: State, player: Player) -> bool:
    for i in range(3):
        if checkColonne(grid, player, i):
            return True
        if checkLigne(grid, player, i):
            return True
    if checkDiagonales(grid, player):
        return True     
    return False  
    

def checkLigne(grid :State, player : Player, num : int)-> bool:
    if (num != 0) and (num != 1) and (num != 2): 
        print("erreur")
        return False 
    for i in range(3):
        if grid[num][i] != player : 
            return False
    return True

def checkColonne(grid :State, player : Player, num : int) -> bool:
    if (num != 0) and (num != 1) and (num != 2): 
        print("erreur")
        return False 
    for i in range(3):
        if grid[i][num] != player :
            return False
    return True


def checkDiagonales(grid :State, player : Player) -> bool:
    Diagonale1 = True
    for i in range(3):
        if grid[i][i] != player :
            Diagonale1 = False
    if Diagonale1 : 
        return True
    for i in range(3):
        if grid[2-i][i] != player :
            return False
    return True



def final(grid: State) -> bool:
    if isfull(grid) or line(grid, 1) or line(grid,2):
        return True
    return False

def isfull(grid:Grid) -> bool:
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                return False
    return True

def score(grid: State) -> float:
    if not final(grid): 
        print("partie pas finie")
        return 0
    if line(grid, 1) : return 1
    if line(grid, 2) : return -1
    if isfull(grid) : return 0
    print("erreur score")
    return 0
    
    
def pprint(grid: State):
    for i in range(len(grid)):
        for j in range(len(grid)):
            a = ''
            if grid[i][j] == 0: a = "0"
            if grid[i][j] == 1: a = "X"
            if grid[i][j] == 2: a = "O"
            print(a," ", end="")
        print("\n")
    return
               
def legals(grid: State) -> list[Action]:
    t = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                a = (i,j)
                t.append(a)
    return t

def play(grid: State, player: Player, action: Action) -> State:
    a = grid_tuple_to_grid_list(grid)
    a[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(a)

def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    player = 1
    while not final(grid):
        pprint(grid)
        print("Au tour du joueur ", player)
        if player == 1:
            grid = play(grid,player, strategy_X(grid, player))
            player = 2
        elif player == 2:
            grid = play(grid,player, strategy_O(grid, player))
            player = 1
    print("Partie terminée \nGrille finale :")
    pprint(grid)
    print("Score : ")
    return score(grid)



######### Strategy / Joueurs

def strategy_random(grid: State, player: Player) -> Action:
    

    return

def strategy_first_legal(grid: State, player: Player) -> Action:
    return legals(grid)[0]


def strategy_brain(grid: Grid, player: Player) -> Action:
    print("à vous de jouer: ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)
    return t        
    
#### Minmax

def minmax(grid: State, player: Player) -> float:
    if final(grid) : return score(grid)
    if player == 1 :
        k = 2
    elif player == 2:
        k = 1
    t = legals(grid)
    t2 = [play(grid,player,action) for action in t]
    t3 = []
    for i in t2:
        t3.append(minmax(i, k))
    if player == 1 :
        return max(t3)
    if player == 2 :
        return min(t3)
    

def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[float, Action]:
    if final(grid) : return (score(grid), (-1,-1))
    if player == 1 : #Maximising player 
        k = 2
    elif player == 2: #Minimising Player
        k = 1
    t = legals(grid)
    t2 = [play(grid,player,action) for action in t]
    t3 = []
    for i in t2:
        t3.append(minmax(i, k))
    if player == 1 :
        n = dernierIndiceMaximum(t3)
        return (t3[n],t[n])
    if player == 2 :
        n = dernierIndiceMinimum(t3)
        return (t3[n],t[n])


	
def dernierIndiceMaximum(liste):
    maxi = liste[0]
    longueur=len(liste)
    indice_max = 0
    for i in range(longueur):
        if liste[i] >= maxi:
            maxi = liste[i]
            indice_max = i
    return indice_max
    

	
def dernierIndiceMinimum(liste):
    maxi = liste[0]
    longueur=len(liste)
    indice_max = 0
    for i in range(longueur):
        if liste[i] <= maxi:
            maxi = liste[i]
            indice_max = i
    return indice_max




def cache(f):
    
    cache = {}
    
    def g(grid, player):
        if grid in cache:
            return cache[grid]
        val = f(grid, player)
        cache[grid] = val
        return val
    return g

@cache 
def strategy_minmax(grid: Grid, player: Player) -> Action:
    return minmax_action(grid,player)[1]

##================ Strategy Alpha Beta ===================================



def alphabeta(grid: State, alpha: int, beta: int, maximizingPlayer: int) -> int:
    if final(grid) : return score(grid)
    if maximizingPlayer == 1:
        value = -10
        t = legals(grid)
        for action in t:
            value = max(value, alphabeta(play(grid,maximizingPlayer,action), alpha, beta, 2))
            alpha = max(alpha, value)
            if alpha >= beta:
                return value
        return value
    
    else: # minimizing player
        value = 10
        t = legals(grid)
        for action in t:
            value = min(value, alphabeta(play(grid,maximizingPlayer,action), alpha, beta, 1))#
            beta = min(beta, value)
            if alpha >= beta:
                return value
        return value


def alpha_beta_action(grid: State, player: Player, depth: int = 0, alpha: int = -10, beta :int = 10) -> tuple[float, Action]:
    if final(grid) : return (score(grid), (-1,-1))
    
#Maximising Player : player == 1 

#Minimising Player : player == 2 
    if player == 1 : #Maximising player 
        k = 2
    elif player == 2: #Minimising Player
        k = 1


    t = legals(grid)
    t2 = [play(grid,player,action) for action in t]
    t3 = []
    
    for i in t2:
        t3.append(alphabeta(i, -10, 10, k))
    
    if player == 1 :
        n = dernierIndiceMaximum(t3)
        return (t3[n],t[n])
    if player == 2 :
        n = dernierIndiceMinimum(t3)
        return (t3[n],t[n])



def strategy_alpha_beta(grid: Grid, player: Player) -> Action:
    
    
    
    return alpha_beta_action(grid, player)[1]


import time

start_time = time.time()


tictactoe(strategy_alpha_beta,strategy_alpha_beta)


print("--- %s seconds ---" % (time.time() - start_time))



## ================= Cache ==========

#def cache(f):
#    
#    cache = {}
#    
 #   def g(state, player):
  #      if state in cache:
   #         return cache(state)
    #    val = f(state, player)
     #   cache[state] = val
      #  return val
    #return g
