# PROJ531 - Application de Gestion et Passation de Quiz en Python

Projet académique réalisé dans le cadre de l'unité d'enseignement **PROJ531 - Gestion de projet informatique** à l'**Université Savoie Mont Blanc**.

---

## 1. Présentation du Projet et Objectifs

Ce projet a pour finalité la conception, le développement et la validation d'une application modulaire en Python dédiée à la création, à l'administration et à la passation de quiz interactifs.

Le développement s'inscrit rigoureusement dans le cadre méthodologique **Agile / Scrum**, en appliquant les bonnes pratiques de génie logiciel :
- Découpage du cycle de vie en sprints itératifs et incrémentaux.
- Séparation stricte des responsabilités (architecture en couches).
- Gestion des versions collaborative et traçabilité des tâches via Git et Kanban.
- Couverture fonctionnelle assurée par une suite de tests unitaires automatisés.

### Fonctionnalités Principales du Système
- **Gestion des Comptes et Authentification :** Inscription et authentification avec contrôle d'accès basé sur les rôles (Joueur et Administrateur).
- **Sécurité Cryptographique :** Protection des mots de passe par hachage SHA-256 associé à un sel cryptographique unique par utilisateur et comparaison à temps constant.
- **Persistance des Données :** Sérialisation structurée au format standard JSON (`users.json`, `quizzes.json`, `results.json`).
- **Administration des Quiz :** Création interactive par saisie console et importation automatisée à partir de fichiers texte structurés.
- **Moteur d'Évaluation :** Déroulement séquentiel des questionnaires, validation des réponses, calcul immédiat du score et restitution des réponses attendues.
- **Historique Individuel :** Enregistrement des résultats pour assurer le suivi des performances des joueurs.

---

## 2. Organisation de l'Équipe et Rôles Scrum

Le projet est conduit par une équipe de 4 étudiants conformément aux rôles Scrum :

| Membre | Rôle Scrum | Responsabilités principales |
| :--- | :--- | :--- |
| **Bilal Draoui** | **Product Owner (PO)** & Développeur | Gestion du produit, interface avec le commanditaire, priorisation du backlog, validation des livrables et des critères d'acceptation. |
| **Sabrine Kawiche** | Développeuse | Modélisation conceptuelle des données (MCD), gestion du dépôt GitHub, développement des modèles de données. |
| **Chadi Kharchoufa** | Développeur | Décomposition WBS, planification temporelle Gantt, conception du module de sécurité et hachage. |
| **Gabrien Vaz** | Développeur | Conception des services applicatifs, persistance des données JSON, développement des suites de tests unitaires. |

Tableau de suivi Kanban (Trello) : [Tableau Trello PROJ531-Quiz-Python](https://trello.com/b/zFAmvu0D/proj531-quiz-python)

---

## 3. Architecture Logicielle et Organisation du Dépôt

Le système repose sur une architecture découplée afin d'assurer l'indépendance entre l'interface utilisateur, la logique métier et la couche d'accès aux données.

```text
PROJ531-Quiz-Python/
├── main.py                            # Point d'entrée exécutable unique
├── README.md                          # Documentation générale et technique
├── .gitignore                         # Exclusions de versionnement (caches, data/, environnements)
├── docs/                              # Dossier de gestion de projet et livrables
│   ├── Gantt_projet_quiz.gan          # Diagramme de Gantt (source GanttProject)
│   ├── Gantt_projet_quiz.png          # Export graphique du planning Gantt
│   ├── wbs_projet_quiz_python.png     # Organigramme de décomposition des tâches (WBS)
│   ├── quiz.mdc                       # Modèle Conceptuel de Données (source Looping)
│   ├── mcd_documentation.md           # Spécifications détaillées du MCD et dictionnaire des données
│   ├── glossaire.md                   # Glossaire terminologique du projet
│   ├── trello_sprint2.png             # Preuve d'avancement Kanban (clôture Sprint 2)
│   └── comptes-rendus/                # Comptes-rendus hebdomadaires de séance
│       ├── cr_seance_1.md             # Séance 1 : Cadrage, WBS, Gantt, MCD
│       ├── cr_seance_2.md             # Séance 2 : Authentification, sécurité, stockage JSON
│       └── cr_seance_3.md             # Séance 3 : Moteur de quiz, création, import et passation
├── src/                               # Code source applicatif
│   ├── cli.py                         # Interface utilisateur en ligne de commande (CLI)
│   ├── security.py                    # Primitives cryptographiques (hachage, salage)
│   ├── models/                        # Entités métier (User, Quiz, Question, Reponse, Resultat)
│   ├── services/                      # Services applicatifs (AuthService, QuizService, StorageService)
│   └── utils/                         # Utilitaires transverses
└── tests/                             # Suites de tests unitaires automatisés
    ├── test_security.py               # Validation de la robustesse cryptographique
    ├── test_auth.py                   # Validation des flux d'authentification
    └── test_storage.py                # Validation de la persistance JSON
```

### Remarque relative aux données locales
Le répertoire `data/` stockant les fichiers JSON (`users.json`, `quizzes.json`, `results.json`) est volontairement exclu du suivi de versions via le fichier `.gitignore` afin de garantir la confidentialité des données et d'éviter les conflits entre environnements de développement. Ce répertoire est initialisé de manière autonome lors du premier lancement de l'application.

---

## 4. Modèle Conceptuel de Données (MCD)

La modélisation Entité-Association a été formalisée selon le formalisme Merise. Le détail des entités, associations et cardinalités est disponible dans [docs/mcd_documentation.md](docs/mcd_documentation.md).

- **Utilisateur (0,n) --- creer --- (1,1) Quiz**
- **Quiz (1,n) --- contenir --- (1,1) Question**
- **Question (2,n) --- proposer --- (1,1) Reponse**
- **Utilisateur (0,n) --- obtenir --- (1,1) Resultat**
- **Quiz (0,n) --- concerner --- (1,1) Resultat**

---

## 5. Spécifications Techniques et Déploiement

### Prérequis d'Exécution
- **Environnement d'exécution :** Python 3.10 ou version supérieure (validé sous Python 3.11).
- **Dépendances tierces :** Aucune bibliothèque externe n'est requise. L'implémentation repose exclusivement sur les modules standards certifiés de Python (`hashlib`, `secrets`, `hmac`, `json`, `uuid`, `unittest`, `getpass`).

### Procédure de Lancement
À la racine du projet, exécuter la commande suivante :
```bash
python main.py
```

### Comptes de Démonstration Pré-configurés
Lors de l'initialisation initiale de la base locale, deux profils de référence sont créés automatiquement :

| Profil | Identifiant (ou Adresse e-mail) | Mot de passe | Rôle attribué |
| :--- | :--- | :--- | :--- |
| **Administrateur** | `admin` (ou `admin@quiz.fr`) | `Admin123!` | Administration du système |
| **Joueur** | `joueur1` (ou `joueur1@quiz.fr`) | `Joueur123!` | Passation de quiz |

La création autonome de nouveaux comptes joueurs est accessible via le menu d'inscription de l'interface console.

---

## 6. Assurance Qualité et Tests Unitaires

Conformément aux exigences de livraison logicielle sans régression, la conformité du code est validée par l'exécution de la suite de tests unitaires :

```bash
python -m unittest discover tests -v
```

Tous les tests doivent obligatoirement être validés préalablement à toute fusion ou livraison vers la branche principale `main`.

---

## 7. Planification et Suivi des Sprints (Roadmap)

Le calendrier du projet est découpé en 4 sprints successifs :

- **Sprint 1 (12/10 - 15/10) : Cadrage et Conception Initiale** - Statut : Validé
  - Initialisation du dépôt Git et de la documentation socle.
  - Modélisation conceptuelle de données (MCD) sous Looping.
  - Établissement de l'organigramme WBS et du diagramme de Gantt (durée maximale de 2 jours par tâche élémentaire).
  - Mise en place du tableau Kanban Trello.

- **Sprint 2 (19/10 - 22/10) : Authentification et Persistance Utilisateurs** - Statut : Validé
  - Architecture modulaire et instanciation des modèles de données.
  - Implémentation du sous-système de sécurité (hachage salé SHA-256).
  - Gestion de la persistance JSON des utilisateurs (`data/users.json`).
  - Interface console de gestion des flux d'inscription et de connexion.
  - Validation de la première suite de tests unitaires automatisés.

- **Sprint 3 (26/10 - 30/10) : Cœur Fonctionnel et Gestion des Quiz** - Statut : En cours
  - Module de création interactive de quiz par l'administrateur (US04).
  - Module d'importation de quiz depuis des fichiers texte structurés (US05).
  - Moteur d'exécution des questionnaires et restitution des scores pour les joueurs (US06).
  - Extension de la couverture de tests unitaires au moteur de jeu.

- **Sprint 4 (02/11 - 06/11) : Historisation des Résultats, Consolidation et Soutenance** - Statut : Planifié
  - Sauvegarde de l'historique individuel des scores par joueur (`results.json`).
  - Audit de robustesse et correction des anomalies éventuelles.
  - Rédaction du rapport final de projet.
  - Préparation et répétition de la soutenance orale (démonstration de 15 minutes).
