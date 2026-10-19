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

Le projet adopte une **architecture en couches modulaires (Layered Architecture)** pour garantir une séparation stricte des responsabilités, une haute maintenabilité et une facilité de test :

```text
PROJ531-Quiz-Python/
├── README.md                          # Documentation principale du dépôt
├── .gitignore                         # Exclusion des fichiers temporaires et caches
├── data/                              # Répertoire de stockage des fichiers JSON
│   ├── users.json                     # Comptes utilisateurs et empreintes sécurisées
│   ├── quizzes.json                   # Définition des quiz et questions
│   └── results.json                   # Historique des scores et passages
├── docs/                              # Dossier de gestion de projet et livrables
│   ├── Gantt_projet_quiz.gan          # Fichier source GanttProject
│   ├── Gantt_projet_quiz.png          # Export image du planning prévisionnel
│   ├── wbs_projet_quiz_python.png     # Organigramme des tâches (WBS)
│   ├── quiz.mdc                       # Fichier source Looping du MCD
│   ├── glossaire.md                   # Glossaire des termes du projet
│   ├── mcd_documentation.md           # Dictionnaire des données et schéma Merise
│   └── comptes-rendus/                # Comptes-rendus hebdomadaires de séance
│       ├── cr_seance_1.md             # Séance 1 (Cadrage et conception)
│       └── cr_seance_2.md             # Séance 2 (Sprint 2 - Authentification)
├── src/                               # Code source de l'application
│   ├── main.py                        # Point d'entrée de l'interface en ligne de commande (CLI)
│   ├── models/                        # Modèles métier (Classes de données)
│   │   ├── user.py                    # Classe User (Joueur / Admin)
│   │   ├── quiz.py                    # Classe Quiz
│   │   ├── question.py                # Classe Question
│   │   ├── reponse.py                 # Classe Reponse
│   │   └── resultat.py                # Classe Resultat
│   ├── services/                      # Logique métier et persistance
│   │   ├── auth_service.py            # Inscription, connexion, sessions
│   │   └── storage_service.py         # Lecture/écriture des fichiers JSON
│   └── utils/                         # Fonctions utilitaires
│       ├── security.py                # Hachage SHA-256 avec sel aléatoire
│       └── validators.py              # Validation d'email, pseudo et mot de passe
└── tests/                             # Suite de tests unitaires automatisés
    ├── test_auth.py                   # Tests du service d'authentification
    ├── test_security.py               # Tests du module cryptographique
    └── test_storage.py                # Tests du service de persistance JSON
```

### Modèle Conceptuel de Données (MCD)
Le schéma complet et le dictionnaire de données sont détaillés dans [docs/mcd_documentation.md](file:///c:/Users/Admin/Desktop/PROJ531-Quiz-Python/docs/mcd_documentation.md).
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
Ouvrez un terminal dans le répertoire racine du projet et exécutez :
```bash
python -m src.main
```
*(ou `python src/main.py`)*

### Comptes de test pré-configurés
Lors du premier lancement, deux comptes de démonstration sont automatiquement créés dans `data/users.json` pour vous permettre d'évaluer directement l'application :

| Rôle | Identifiant (ou Email) | Mot de passe | Accès et permissions |
| :--- | :--- | :--- | :--- |
| **Administrateur** | `admin` (ou `admin@quiz.fr`) | `Admin123!` | Espace administration, gestion quiz, listing utilisateurs |
| **Joueur** | `joueur1` (ou `joueur1@quiz.fr`) | `Joueur123!` | Espace joueur, passation de quiz, consultation scores |

Vous pouvez également créer à tout moment un nouveau compte joueur via le menu **2. S'inscrire**.

---

## 🧪 5. Validation & Tests Unitaires

Conformément à l'exigence d'Open Source sans bug exigée par le sujet, le projet intègre une suite de tests unitaires automatisés validant tous les scénarios nominaux et d'erreur (format des mots de passe, doublons, résistance aux attaques temporelles, sérialisation).

Pour exécuter tous les tests unitaires :
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
- [x] **Sprint 2 (19/10 - 22/10) : Authentification & Stockage**
  - [x] Architecture modulaire et modèles POO (`User`, `Quiz`, `Question`, `Reponse`, `Resultat`)
  - [x] Sécurité : Hachage SHA-256 avec sel cryptographique
  - [x] Persistance JSON (`data/users.json`)
  - [x] Interface CLI de connexion / inscription avec menus dédiés
  - [x] Suite de tests unitaires automatisés (`15 tests passés avec succès`)
- [ ] **Sprint 3 (26/10 - 30/10) : Cœur du Jeu & Création de Quiz**
  - [ ] Création manuelle d'un quiz par l'administrateur
  - [ ] Importation de quiz depuis un fichier texte
  - [ ] Sélection et passation d'un quiz par un joueur avec validation des réponses
- [ ] **Sprint 4 (02/11 - 06/11) : Scores, Finitions & Soutenance**
  - [ ] Calcul et persistance des scores dans `results.json`
  - [ ] Historique individuel des scores par joueur
  - [ ] Rédaction du rapport final de projet
  - [ ] Répétition de la démonstration de soutenance (15 min)
