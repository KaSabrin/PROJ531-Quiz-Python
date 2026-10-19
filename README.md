# 🎓 PROJ531 – Application de Gestion et Passation de Quiz en Python

Projet universitaire réalisé dans le cadre de l'UE **PROJ531 - Gestion de projet informatique** à l'**Université Savoie Mont Blanc**.

---

## 📌 1. Présentation et Objectifs du Projet

L'objectif de ce projet est de concevoir et développer une application complète en Python permettant la **création, l'administration et la passation de quiz interactifs**, tout en appliquant les principes rigoureux de la **gestion de projet en méthode Agile / Scrum**.

### ✨ Fonctionnalités Principales
- **Système d'Authentification & Rôles :** Inscription et connexion sécurisées distinguant les rôles **Joueur** et **Administrateur**.
- **Sécurité des Données :** Hachage cryptographique des mots de passe avec **SHA-256 salé** (sel unique par utilisateur) et comparaison à temps constant.
- **Persistance des Données :** Stockage modulaire au format standardisé **JSON** (`users.json`, `quizzes.json`, `results.json`).
- **Administration des Quiz :** Création manuelle interactive et importation automatisée depuis des fichiers texte structurés.
- **Moteur de Jeu & Évaluation :** Passation de quiz pour les utilisateurs autorisés, calcul immédiat du score, restitution des bonnes réponses et historisation des résultats.

---

## 👥 2. Composition de l'Équipe & Rôles Scrum

Le projet est mené en équipe de 4 étudiants selon le cadre Scrum :

| Nom / Étudiant | Rôle Scrum | Responsabilités principales |
| :--- | :--- | :--- |
| **Bilal Draoui** | **Product Owner (PO)** & Dév | Interface avec le commanditaire (enseignant), vision produit, priorisation du backlog, validation des livrables. |
| **Sabrine Kawiche** | Développeuse | Conception du MCD, gestion du dépôt GitHub, développement des modèles de données. |
| **Chadi Kharchoufa** | Développeur | Élaboration du WBS, planification Gantt, conception de la sécurité et du hachage. |
| **Gabrien Vaz** | Développeur | Développement des services applicatifs, persistance JSON, conception des tests unitaires. |

> 🔗 **Tableau Trello de suivi des tâches :** [Tableau Trello PROJ531-Quiz-Python](https://trello.com/b/zFAmvu0D/proj531-quiz-python)

---

## 🏛️ 3. Architecture Logicielle & Modèle de Données

Le projet adopte une **architecture en couches** (modèles / services / utilitaires / interface) pour séparer les responsabilités et faciliter les tests.

> 🟡 Le code applicatif (`src/`, `tests/`) est en cours de développement dans le cadre du **Sprint 2** et sera publié sur le dépôt à la fin du sprint. L'arborescence ci-dessous est la structure **cible**.

```text
PROJ531-Quiz-Python/
├── main.py                            # Point d'entrée unique : python main.py
├── README.md                          # Documentation principale du dépôt
├── .gitignore                         # Fichiers exclus de Git (caches, data/, .env)
├── docs/                              # Gestion de projet et livrables
│   ├── Gantt_projet_quiz.gan          # Planning (source GanttProject)
│   ├── Gantt_projet_quiz.png          # Planning (image)
│   ├── wbs_projet_quiz_python.png     # Organigramme des tâches (WBS)
│   ├── quiz.mdc                       # MCD (source Looping)
│   ├── mcd_documentation.md           # MCD expliqué + dictionnaire des données
│   ├── glossaire.md                   # Glossaire du projet
│   └── comptes-rendus/                # Un compte-rendu par séance
│       ├── cr_seance_1.md
│       └── cr_seance_2.md
├── src/                               # Code source (Sprint 2, en cours)
│   ├── cli.py                         # Menus de l'interface console
│   ├── models/                        # Classes de données (User, Quiz, Question, Reponse, Resultat)
│   ├── services/                      # Authentification et stockage JSON
│   └── utils/                         # Sécurité (hachage) et validation des saisies
└── tests/                             # Tests unitaires (uniquement des fichiers test_*.py)
```

> Le dossier `data/` (fichiers `users.json`, `quizzes.json`, `results.json`) **n'est pas versionné** : il est exclu par le `.gitignore` pour ne pas publier les comptes utilisateurs, et il est recréé automatiquement au premier lancement.

### Modèle Conceptuel de Données (MCD)
Le schéma complet et le dictionnaire de données sont détaillés dans [docs/mcd_documentation.md](docs/mcd_documentation.md).
- `Utilisateur (0,n) --- creer --- (1,1) Quiz`
- `Quiz (1,n) --- contenir --- (1,1) Question`
- `Question (2,n) --- proposer --- (1,1) Reponse`
- `Utilisateur (0,n) --- obtenir --- (1,1) Résultat`
- `Quiz (0,n) --- concerner --- (1,1) Résultat`

---

## 🚀 4. Installation et Démarrage

### Prérequis
- **Python 3.10 ou supérieur** (testé avec succès sous Python 3.11).
- Aucune dépendance externe tierce n'est requise : le projet utilise exclusivement la bibliothèque standard de Python (`hashlib`, `secrets`, `hmac`, `json`, `uuid`, `unittest`, `getpass`).

### Lancement de l'application
Ouvrez un terminal à la racine du projet et exécutez :
```bash
python main.py
```

### Comptes de test pré-configurés
Au premier lancement, deux comptes de démonstration sont créés automatiquement dans `data/users.json` :

| Rôle | Identifiant (ou Email) | Mot de passe |
| :--- | :--- | :--- |
| **Administrateur** | `admin` (ou `admin@quiz.fr`) | `Admin123!` |
| **Joueur** | `joueur1` (ou `joueur1@quiz.fr`) | `Joueur123!` |

Un nouveau compte joueur peut aussi être créé via le menu **2. S'inscrire**.

---

## 🧪 5. Tests Unitaires

Les tests unitaires (en cours d'écriture pendant le Sprint 2) se lancent avec :
```bash
python -m unittest discover tests -v
```

---

## 📅 6. Feuille de Route des Sprints (Roadmap)

- [x] **Sprint 1 (12/10 - 15/10) : Cadrage et Conception**
  - [x] Création du dépôt Git et premier README
  - [x] Conception du MCD sur Looping
  - [x] Organigramme WBS et planning Gantt (tâches $\le 2$ jours)
  - [x] Initialisation du tableau Kanban Trello
- [ ] **Sprint 2 (19/10 - 22/10) : Authentification & Stockage** — 🟡 *en cours*
  - [ ] Architecture du code et modèles (`User`, `Quiz`, `Question`, `Reponse`, `Resultat`)
  - [ ] Sécurité : hachage SHA-256 avec sel
  - [ ] Stockage JSON des utilisateurs
  - [ ] Menu console de connexion / inscription
  - [ ] Tests unitaires
- [ ] **Sprint 3 (26/10 - 30/10) : Cœur du Jeu & Création de Quiz**
  - [ ] Création manuelle d'un quiz par l'administrateur
  - [ ] Importation de quiz depuis un fichier texte
  - [ ] Sélection et passation d'un quiz par un joueur avec validation des réponses
- [ ] **Sprint 4 (02/11 - 06/11) : Scores, Finitions & Soutenance**
  - [ ] Calcul et persistance des scores dans `results.json`
  - [ ] Historique individuel des scores par joueur
  - [ ] Rédaction du rapport final de projet
  - [ ] Répétition de la démonstration de soutenance (15 min)
