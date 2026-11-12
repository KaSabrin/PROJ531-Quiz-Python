# Règles de travail Git - Quizora

Ces règles ont été adoptées en fin de projet (séance 5) après un conflit sur `src/cli.py` causé par des modifications faites directement sur `main`.

## Branches

| Branche | Rôle |
| :--- | :--- |
| `main` | Version livrée. Elle doit toujours fonctionner et passer tous les tests. On n'y travaille jamais directement. |
| `dev-bilal`, `dev-sabrine`, `dev-chadi`, `dev-gabrien` | Branche de travail de chaque membre. |

## Travailler sur une tâche

```bash
git switch dev-<prenom>                # se placer sur sa branche
git pull origin main                   # récupérer la dernière version de main
# ... modifier le code ...
python -m unittest discover tests      # tous les tests doivent passer
git add <fichiers>
git commit -m "feat: description courte de la modification"
git push origin dev-<prenom>
```

Ensuite, sur GitHub : **Pull requests > New pull request**, base `main`, compare `dev-<prenom>`. Un autre membre relit la Pull Request, puis la fusionne (**Merge**).

## Messages de commit

Un préfixe indique le type de modification :

| Préfixe | Usage | Exemple |
| :--- | :--- | :--- |
| `feat:` | Nouvelle fonctionnalité | `feat: historique des scores du joueur` |
| `fix:` | Correction de bug | `fix: plantage si le fichier d'import est un PDF` |
| `test:` | Ajout ou modification de tests | `test: refus des titres de quiz en double` |
| `docs:` | Documentation, comptes rendus | `docs: compte rendu de la séance 5` |

## À ne jamais versionner

Le dossier `data/` (comptes et scores locaux) et les caches Python sont exclus par `.gitignore`.
