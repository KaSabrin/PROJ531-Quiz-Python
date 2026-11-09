# Scénario de la démonstration - Quizora (15 minutes)

Déroulé de la démonstration finale demandée par le sujet. La colonne « Présenté par » est à remplir par l'équipe.

## Préparation (avant de passer)

```bash
git pull
python -m unittest discover tests     # doit afficher : Ran 30 tests ... OK
```

- Supprimer le dossier `data/` pour repartir de zéro : il est recréé au lancement avec les comptes de démonstration et les 3 quiz d'exemple.
- Garder ouverts : le terminal, le dépôt GitHub, le tableau Trello et `docs/rapport_final.pdf`.

| Compte | Identifiant | Mot de passe |
| :--- | :--- | :--- |
| Administrateur | `admin` | `Admin123!` |
| Joueur | `joueur1` | `Joueur123!` |

## Déroulé

| Temps | Étape | Ce qu'on montre | Présenté par |
| :---: | :--- | :--- | :--- |
| 0:00 - 2:00 | **Présentation** | Le sujet, l'équipe et les rôles (Product Owner, développeurs), l'objectif de Quizora. | |
| 2:00 - 4:00 | **Gestion de projet** | Le WBS, le PBS et le Gantt (`docs/`), le tableau Trello, un compte rendu de séance, l'historique des commits sur GitHub. | |
| 4:00 - 6:00 | **Administrateur (console)** | `python main.py` → connexion `admin` → import de `sample_quiz.txt` (option 4) → création rapide d'un quiz à 1 question (option 3). | |
| 6:00 - 9:00 | **Joueur (console)** | Déconnexion → connexion `joueur1` → passer un quiz en faisant volontairement une erreur → score final et correction → historique des scores (option 3). | |
| 9:00 - 11:00 | **Interface graphique** | `python gui_main.py` → connexion `joueur1` → bouton « Jouer » sur un quiz → résultat → « Mon historique de scores ». | |
| 11:00 - 12:30 | **Architecture et qualité** | Schéma en couches (`docs/architecture_technique_quizora.pdf`) : la console et la GUI utilisent les mêmes services. Lancement des 30 tests. Mots de passe hachés et salés dans `data/users.json`. | |
| 12:30 - 15:00 | **Bilan et questions** | Ce qui fonctionne, ce qu'on améliorerait (branches et Pull Requests, GitHub Actions, minuterie, export JSON), puis questions de l'enseignant. | |

## En cas de problème pendant la démo

| Problème | Solution |
| :--- | :--- |
| Mauvais mot de passe ou compte introuvable | Supprimer `data/` et relancer : les comptes de démonstration sont recréés. |
| La fenêtre graphique ne s'ouvre pas | Continuer la démonstration en console, qui offre les mêmes fonctionnalités. |
| Fichier d'import introuvable | Lancer l'application depuis le dossier `PROJ531-Quiz-Python` et saisir `sample_quiz.txt` ou `exemples/quiz_python.txt`. |
