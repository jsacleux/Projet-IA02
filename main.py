import matrice
import gopher
import commons
import newgopher

##Explication : comment passer de coordonnés de matrice (0 -> 14) aux coordonnés de la grille (-6 -> 6)
# Exemple d'un exagone de taille 6 : on a une matrice de taille 13/13
# matrice[0][0] = hexagone[6][-6]
# matrice[6][6] = hexagone[0][0]
# matrice[12][12] = hexagone[-6][6]

# matrice[a][b] = hexagone[a+6][b-6]
# matrice[a][b] = hexagone[a+size_hex][b-size_hex]

# matrice[x-6][b+6] = hexagone[x][y]
# matrice[a-size_hex][b+size_hex] = hexagone[x][y]



#######
Joueur1 = 1
Joueur2 = 2
ExempleState1 = [((0,0),Joueur1),((1,1),Joueur2),((1,2),Joueur1),((-1,1),Joueur2)]
ExempleState2 = [((3,2),Joueur1)]

#######


def test():



    ExempleState3 = [((0, 0), Joueur1), ((1, 1), Joueur2)]
    ExempleState4 = [((0, 0), Joueur1), ((1, 1), Joueur2), ((1, 2), Joueur1), ((-1, 1), Joueur2)]
    print(newgopher.get_lastmove(ExempleState3,ExempleState4))

    #gopher.partieGopher(gopher.strategy_gopher_random,gopher.strategy_gopher_random,8)




    a = matrice.creermatrice(6)
    matrice.afficher_matrice(a)
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] != -1 :
                print(matrice.coordMatricetoHex((i,j),5))




    #
    # for i in gopher.gopherlegals(a, ExempleState1, Joueur1)[1]:
    #    gopher.play_gopher(a, i, 4)
    #
    # matrice.afficher_matrice(a)
    #
    # print(" 0,0 : ",matrice.coordHextoMatrice((0,0),7), matrice.coordMatricetoHex((7,7),7))
    # print(" 1,0 : ",matrice.coordHextoMatrice((1, 0), 7), matrice.coordMatricetoHex((6,7),7))
    # print(" 0,1 : ",matrice.coordHextoMatrice((0, 1), 7), matrice.coordMatricetoHex((7,8,),7))
    # print(" 1,1 : ",matrice.coordHextoMatrice((1, 1), 7), matrice.coordMatricetoHex((6,8,),7))
    # print(" -2,-2 : ",matrice.coordHextoMatrice((-2, -2), 7), matrice.coordMatricetoHex((9,5),7))
    #
    # print(matrice.getadjacenthex((-1,2)))
    # #afficher_matrice(a)
    return

if __name__ == '__main__':

    test()