import matrice
import gopher
import commons

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


#######
def test():
    a = matrice.set_matrice_to_state(matrice.creermatrice(7), ExempleState1)
    matrice.afficher_matrice(a)



    f = {
        "clé" : "porte",
    (2,5) : "fenêtre"


    }

    print(f[(2,5)])


    #print(getadjacenthex((1,2)))
    #for i in getadjacenthex((1,2)):
    #    play(a, i, 3)

    #afficher_matrice(a)




    for i in gopher.gopherlegals(a, ExempleState1, Joueur1)[0]:
       gopher.play_gopher(a, i, 4)

    matrice.afficher_matrice(a)


    print(" 0,0 : ",matrice.coordHextoMatrice((0,0),7), matrice.coordMatricetoHex((7,7),7))
    print(" 1,0 : ",matrice.coordHextoMatrice((1, 0), 7), matrice.coordMatricetoHex((6,7),7))
    print(" 0,1 : ",matrice.coordHextoMatrice((0, 1), 7), matrice.coordMatricetoHex((7,8,),7))
    print(" 1,1 : ",matrice.coordHextoMatrice((1, 1), 7), matrice.coordMatricetoHex((6,8,),7))
    print(" -2,-2 : ",matrice.coordHextoMatrice((-2, -2), 7), matrice.coordMatricetoHex((9,5),7))


    print(matrice.getadjacenthex((-1,2)))
    #afficher_matrice(a)
    return

if __name__ == '__main__':

    test()