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
ExempleState2 = [((3,2),Joueur1)]

#######


def test():

    matriceAffichage = matrice.creermatrice(9)
    matrice.set_matrice_to_state(matriceAffichage,ExempleState2)
    enviro = {}
    enviro["game"] = "gopher"
    enviro["hex_size"] = 9
    enviro["gopherJoueur1casesbloquees"] = {}
    enviro["gopherJoueur1casesaccessibles"] = {}
    enviro["gopherJoueur2casesbloquees"] = {}
    enviro["gopherJoueur2casesaccessibles"] = {}

    matrice.afficher_matrice(matriceAffichage)

    for i in range(5):
        print("Coup du joueur 2 : ")
        coupJoueur2 = gopher.strategy_gopher_random(enviro,ExempleState2,Joueur2,4)[1]
        print("Etape 1")
        ExempleState2.append(coupJoueur2)
        gopher.play_gopher(matriceAffichage,coupJoueur2[0], coupJoueur2[1])
        matrice.afficher_matrice(matriceAffichage)
        print("Coup du joueur 1 : ")
        coupJoueur1 = gopher.strategy_gopher_random(enviro,ExempleState2,Joueur1,4)[1]
        print("Etape 2")
        ExempleState2.append(coupJoueur1)
        gopher.play_gopher(matriceAffichage,coupJoueur1[0], coupJoueur1[1])
        matrice.afficher_matrice(matriceAffichage)




    # a = matrice.set_matrice_to_state(matrice.creermatrice(7), ExempleState1)
    # matrice.afficher_matrice(a)
    #
    #
    #
    #
    #
    # for i in gopher.gopherlegals(a, ExempleState1, Joueur1)[1]:
    #    gopher.play_gopher(a, i, 4)
    #
    # matrice.afficher_matrice(a)
    #
    #
    # print(" 0,0 : ",matrice.coordHextoMatrice((0,0),7), matrice.coordMatricetoHex((7,7),7))
    # print(" 1,0 : ",matrice.coordHextoMatrice((1, 0), 7), matrice.coordMatricetoHex((6,7),7))
    # print(" 0,1 : ",matrice.coordHextoMatrice((0, 1), 7), matrice.coordMatricetoHex((7,8,),7))
    # print(" 1,1 : ",matrice.coordHextoMatrice((1, 1), 7), matrice.coordMatricetoHex((6,8,),7))
    # print(" -2,-2 : ",matrice.coordHextoMatrice((-2, -2), 7), matrice.coordMatricetoHex((9,5),7))
    #
    #
    # print(matrice.getadjacenthex((-1,2)))
    # #afficher_matrice(a)
    return

if __name__ == '__main__':

    test()