# Projet IA02 : 

Implémentation de stratégies pour les jeux Dodo et Gopher (Mark Steere) par Gautier MIRALLES et Juliette SACLEUX.


# Guide utilisateur

## Mise en place

1. Mettez tous nos fichiers dans votre repertoire de travail
2. Si votre machine n'est pas très performante, diminuez env["n_simulations"] dans la fonciton initialize de test_client.py pour éviter les Time Out. 

## Exécution

1. Lancer le serveur
2. Si besoin, modifier l'adresse du serveur dans test_client.py (par défaut c'est http://localhost:8080/)
3. Lancer le client `test_client.py` avec 3 argument : le numéro de groupe, le nom, et le mot de passe.

```bash
# lancer le client
python test_client.py 12 toto totovelo
```
