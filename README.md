# Quizora - Application de Gestion et Passation de Quiz en Python

Projet académique réalisé dans le cadre de l'unité d'enseignement **PROJ531 - Gestion de projet informatique** à l'**Université Savoie Mont Blanc**.

---

## 1. Présentation du Projet

**Quizora** est une application console en Python développée par notre groupe dans le cadre du module **PROJ531 (Gestion de projet informatique)** à l'Université Savoie Mont Blanc.

Elle permet de gérer et de passer des quiz sous forme de QCM :
- **Comptes et sécurité :** Inscription et connexion avec distinction des rôles (Joueur et Administrateur). Les mots de passe sont hachés en SHA-256 avec un sel individuel de 16 octets.
- **Gestion des quiz :** L'administrateur peut créer des quiz directement dans le terminal ou les importer depuis un fichier texte `.txt`.
- **Passation et scores :** Le joueur choisit un quiz, répond aux questions, et l'application affiche son score et les bonnes réponses.
- **Stockage local :** Les données sont enregistrées dans des fichiers JSON (`users.json`, `quizzes.json`, `results.json`) dans un dossier `data/`.
- **Méthode Agile :** Le travail est découpé en 4 sprints de 2 jours maximum par tâche, suivis sur Trello et planifiés sur un diagramme de Gantt.

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
│   ├── architecture_technique_quizora.pdf  # Dossier d'architecture technique (PDF certifié)
│   ├── architecture_technique_quizora.md   # Spécifications et schéma d'architecture Mermaid
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
L'application propose deux modes d'exécution (sans aucune dépendance externe à installer) :

1. **Mode Interface Graphique (GUI - Page de connexion et tableau de bord moderne) :**
```bash
python gui_main.py
# ou
python main.py --gui
```

2. **Mode Console classique (CLI interactif en terminal) :**
```bash
python main.py
```
*(Le mode console permet également d'ouvrir l'interface graphique via l'option 4 du menu d'accueil).*

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
