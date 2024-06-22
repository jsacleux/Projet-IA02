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
