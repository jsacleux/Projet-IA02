from basic_types import State

def creermatrice(n : int):
    matrice = [[ 0 for i in range(2*n - 1)] for i in range(2 * n -1)]

    for i in range(0, n):
        for j in range(0, n - i):
            matrice[i][j] = -1

    for i in range(0, n):
        for j in range(2 * n - 2 - i, 2 * n - 1):
            matrice[n-1 + i][j] = -1
    for i in range(n*2-1):
        matrice[0][i] = -1
        matrice[-1][i] = -1
        matrice[i][0] = -1
        matrice[i][-1] = -1

    return matrice


def set_matrice_to_state(matrice, state: State):
    for i in state:
        set_pion_in_matrice(matrice, i[0], i[1])
    return matrice


def set_pion_in_matrice(matrice, coup, joueur):   #(grid: State, player: Player, action: Action) -> State :
    sizeGrid = int((len(matrice) + 1) / 2)
    (x, y) = coordHextoMatrice((coup[0], coup[1]), sizeGrid)
    print(x, y, " ", coup[0], coup[1])
    valeur = matrice[x][y]
    if valeur != -1 and valeur != 1 and valeur != 2:
        matrice[x][y] = joueur
    elif valeur == -1:
        print("coup hors du plateau")
    else:
        print("case déjà occupé")
    return 0

def afficher_matrice(matrice):
    # Couleurs spécifiques pour chaque valeur utilisant les séquences d'échappement ANSI
    couleurs = {
        1: '\033[91m',  # Rouge
        2: '\033[94m',  # Bleu
        0: '\033[97m',  # Blanc
        -1: '\033[90m'  # Gris
    }
    reset_couleur = '\033[0m'  # Réinitialiser la couleur
    sizeGrid = int((len(matrice) + 1) / 2)

    # Obtenir les dimensions de la matrice
    n_rows = len(matrice)
    n_cols = len(matrice[0]) if n_rows > 0 else 0

    # Calculer la longueur maximale des éléments pour aligner correctement les coordonnées
    max_element_length = max(len(str(matrice[i][j])) for i in range(n_rows) for j in range(n_cols))

    # Afficher les colonnes avec les coordonnées
    print(" " * (max_element_length + 3), end='')  # Espaces pour les coordonnées de ligne
    for j in range(n_cols):
        print(f"{j-sizeGrid+1:>{max_element_length}}", end=' ')
    print()  # Nouvelle ligne

    # Afficher les lignes avec les coordonnées et les éléments de la matrice
    for i in range(n_rows):
        print(f"{-(i-sizeGrid+1):>{max_element_length}} |", end=' ')  # Coordonnées de ligne
        for j in range(n_cols):
            valeur = matrice[i][j]
            couleur = couleurs.get(valeur, '')  # Obtenir la couleur ou utiliser la couleur par défaut
            print(f"{couleur}{valeur:>{max_element_length}}{reset_couleur}", end=' ')
        print()  # Nouvelle ligne
    print()

def getadjacenthex(case):
    ## Attention, coordonnés hexagonaux en entrée, hex en sortie
    a = case[0]
    b = case[1]
    return ((a, b+1),(a+1, b+1),(a+1, b),(a-1, b),(a-1, b-1),(a, b-1))

def coordHextoMatrice(a : tuple[int, int], hexsize :int):
    return (-a[0]+hexsize-1,a[1]+hexsize-1)


def coordMatricetoHex(a : tuple[int, int], hexsize : int):
    return ((-a[0]+hexsize,a[1]-hexsize))
