# Projet IA02 : 

Implémentation de stratégies pour les jeux Dodo et Gopher (Mark Steere) par Gautier MIRALLES et Juliette SACLEUX.


# Guide utilisateur

## Mise en place

1. Placer tous nos fichiers dans votre repertoire de travail
2. Si l'algorithme prend trop de temps, vous pouvez diminuez env["n_simulations"] dans la fonction initialize de `test_client.py`. Pendant la compétition, nous avons utilisé les valeurs fournies, mais si vous êtes préssé(e) ou que votre machine est moins performante et que vous avez des Timeout, les performances restent bonnes (contre random) en diminuant ces valeurs (par exemple divisé par 10).

## Exécution

1. Lancer le serveur
2. Si besoin, modifier l'adresse du serveur dans `test_client.py` (par défaut l'adresse est http://localhost:8080/)
3. Lancer le client `test_client.py` avec 3 arguments : un numéro, un nom, et un mot de passe.

```bash
# lancer le client
python test_client.py 12 toto totovelo
```
