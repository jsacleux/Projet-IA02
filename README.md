# Projet IA02 : 

Implémentation de stratégies pour les jeux **Dodo** et **Gopher** (Mark Steere) développée par **Gautier MIRALLES** et **Juliette SACLEUX** dans le cadre de l'UV IA02, au semestre P24, groupe 8.

Nous utilisons principalement une stratégie basée sur les Arbres de Recherche de Monte Carlo (MCTS), sauf dans certains cas spécifiques (premier coup, temps restant faible, taille impaire pour Gopher en tant que joueur 1...).

# Guide utilisateur

## Mise en place

1. Placer tous nos fichiers dans votre repertoire de travail
2. Si l'algorithme est trop lent, vous pouvez diminuer la valeur de `env["n_simulations"]` dans la fonction `initialize` du fichier `test_client.py`. Pendant la compétition, nous avons utilisé les valeurs fournies, mais si vous êtes préssé(e) ou que votre machine est moins performante et que vous avez des Timeout, les performances restent bonnes (contre random) en diminuant ces valeurs.

## Exécution

1. Démarrez le serveur.
2. Si besoin, modifiez l'adresse du serveur dans `test_client.py` (par défaut l'adresse est http://localhost:8080/)
3. Lancer le client `test_client.py` avec 3 arguments : un numéro, un nom, et un mot de passe.

```bash
# lancer le client
python test_client.py 12 toto totovelo
```

# Les forces et faiblesses de notre projet

### Les plus de notre projet :
- **Performances** en termes de victoires. Nous gagnons toujours contre random et avons souvent gagné contre les autres groupes pendant le tournoi.
- Implémentation de la **stratégie optimale** dans le cas d'un gopher sur une grille de taille impaire en tant que joueur 1. Dans ce cas, nous sommes surs de gagner.
- **Simplicité**. Dans le cas général, nous utilisons une version très simple de MCTS, ce qui rend notre implémentation facile à comprendre et à debugger. 
- **Performances temporelles**. Nous avons essayer de minimiser les compéxités temporelles de nos fonctions. Nous avons essayé d'employer les structures de données les plus pertinentes en fonction du besoin (set, list, dict). Grâce à cela, nous ne sommes même pas rentrés dans notre garde fou qui joue aléatoirement lorsqu'il reste moins de 8 secondes. 

### Les moins de notre projet :
- Absence de mécanismes d'**apprentissage** des erreurs au fil des parties.

### Les éléments à nuancer  :
- **Performances et simplicité**. Nous avons gagné la plupart de nos matchs mais pas tous. On aurait peut être eu des résultats encore meilleurs avec une version plus complexe du MCTS (par exemple, on ne fait pas varier notre facteur d'exploration).
- **Performances temporelles**. Nos performances temporelles étaient amplement suffisantes pour les besoins du tournoi. De ce fait, nous n'avons pas essayé d'implementer d'autres solutions pour les améliorer. Si nous en avions eu besoins, nous aurions pu utiliser du cache, ou adapter le nombre de simulations dans MCTS en fonction du temps restant.

