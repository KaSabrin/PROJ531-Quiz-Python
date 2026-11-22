# Scénario de la démonstration - Quizora (15 minutes)

Déroulé de la démonstration finale demandée par le sujet. Les présentateurs suivent le script de soutenance de l'équipe.

## Préparation (avant de passer)

```bash
git pull
python -m unittest discover tests     # doit afficher : Ran 39 tests ... OK
```

- Supprimer le dossier `data/` pour repartir de zéro : il est recréé au lancement avec les comptes de démonstration et les 3 quiz d'exemple.
- Garder ouverts : le terminal, le dépôt GitHub, le tableau Trello et `docs/rapport_final.pdf`.

| Compte | Identifiant | Mot de passe |
| :--- | :--- | :--- |
| Administrateur | `admin` | `Admin123!` |
| Joueur | `joueur1` | `Joueur123!` |

## Déroulé

Ordre et textes : script de soutenance de Sabrin (14 diapositives, 15 minutes).

| Temps | Diapositives | Contenu | Présenté par |
| :---: | :--- | :--- | :--- |
| 0:00 - 3:10 | 1 à 4 | Présentation, objectifs, cahier des charges, répartition des responsabilités | Bilal |
| 3:10 - 6:25 | 5 à 7 | PBS et WBS, organisation en sprints, suivi avec Trello et GitHub | Gabrien |
| 6:25 - 7:30 | 8 | Difficultés rencontrées et décisions prises | Chadi |
| 7:30 - 9:40 | 9 et 10 | MCD, architecture modulaire | Sabrin |
| 9:40 - 11:25 | 11 et 12 | Choix techniques, 39 tests automatisés | Chadi |
| 11:25 - 14:15 | 13 | Démonstration : admin (import de `sample_quiz.txt`, création d'un quiz), joueur (quiz avec une erreur volontaire, score, historique) | Sabrin |
| 14:15 - 15:00 | 14 | Bilan, perspectives, questions | Bilal |

## En cas de problème pendant la démo

| Problème | Solution |
| :--- | :--- |
| Mauvais mot de passe ou compte introuvable | Supprimer `data/` et relancer : les comptes de démonstration sont recréés. |
| La fenêtre graphique ne s'ouvre pas | Continuer la démonstration en console, qui offre les mêmes fonctionnalités. |
| Import refusé : « Un quiz intitulé ... existe déjà » | Normal : un même titre n'est importé qu'une fois. Supprimer `data/` avant la démo pour pouvoir importer `sample_quiz.txt`. |
| Fichier d'import introuvable | Lancer l'application depuis le dossier `PROJ531-Quiz-Python` et saisir `sample_quiz.txt`. |
