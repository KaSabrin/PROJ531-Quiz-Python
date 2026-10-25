# Architecture Technique & Structure Logicielle - Quizora

> **Version PDF téléchargeable :** [Consulter le document PDF officiel (docs/architecture_technique_quizora.pdf)](architecture_technique_quizora.pdf)

---

## 1. Schéma d'Architecture en Couches (Mermaid)

```mermaid
graph TD
    subgraph CP["1. Couche Présentation (CLI Console & GUI Tkinter)"]
        MAIN["main.py / gui_main.py<br/>(Points d'entrée exécutables)"]
        CLI_J["cli.py & gui.py - Espace Joueur<br/>(Connexion, passation & scores)"]
        CLI_A["cli.py & gui.py - Espace Admin<br/>(Création manuelle & Import .txt)"]
    end

    subgraph CS["2. Couche Logique Métier & Services"]
        AUTH["AuthService<br/>(Inscription, Connexion, Sessions)"]
        QUIZ["QuizService<br/>(Gestion CRUD & Parseur texte .txt)"]
        STOR["StorageService<br/>(I/O JSON Atomiques UTF-8)"]
    end

    subgraph CSEC["3. Couche Sécurité & Primitives"]
        SECU["security.py<br/>(SHA-256 salé, secrets.token_hex, hmac constant time)"]
    end

    subgraph CMD["4. Couche Modèles de Données (MCD Merise)"]
        MOD_U["User<br/>(pseudo, email, mdp_hash, role)"]
        MOD_Q["Quiz<br/>(titre, description, auteur_id)"]
        MOD_QU["Question<br/>(énoncé, points)"]
        MOD_R["Reponse<br/>(libellé, est_correct)"]
        MOD_RES["Resultat<br/>(score, total, date)"]
    end

    subgraph CD["5. Couche Persistance des Données (JSON)"]
        DATA_U[("data/users.json<br/>Comptes utilisateurs")]
        DATA_Q[("data/quizzes.json<br/>Banque de quiz")]
        DATA_R[("data/results.json<br/>Historique des scores")]
        DATA_T["data/sample_quiz.txt<br/>Importation texte"]
    end

    %% Interactions
    MAIN --> CLI_J
    MAIN --> CLI_A
    CLI_J --> AUTH
    CLI_A --> AUTH
    CLI_J --> QUIZ
    CLI_A --> QUIZ

    AUTH --> SECU
    AUTH --> MOD_U
    AUTH --> STOR

    QUIZ --> MOD_Q
    MOD_Q --> MOD_QU
    MOD_QU --> MOD_R
    QUIZ --> STOR
    QUIZ --> DATA_T

    STOR --> DATA_U
    STOR --> DATA_Q
    STOR --> DATA_R
```

---

## 2. Synthèse de la Stack Technologique

| Domaine | Outil / Technologie | Rôle dans l'application Quizora |
| :--- | :--- | :--- |
| **Langage & Runtime** | Python 3.10+ | Langage principal imposé, typage avec Type Hinting. |
| **Interface Utilisateur** | Console CLI & Tkinter (GUI) | Deux modes d'exécution natifs : terminal interactif (`cli.py`) et fenêtre graphique moderne (`gui.py`). |
| **Sécurité Cryptographique** | `hashlib`, `secrets`, `hmac` | Hachage SHA-256 salé avec sel cryptographique aléatoire de 16 octets et comparaison à temps constant. |
| **Persistance** | `json` (Bibliothèque standard) | Stockage portable et transparent avec encodage UTF-8 forcé. |
| **Assurance Qualité** | `unittest` | Tests unitaires automatisés d'intégration et de non-régression. |
| **Gestion de Versions** | Git & GitHub | Collaboration à 4 étudiants, revue de code, traçabilité des commits. |
| **Suivi Agile** | Trello (Kanban) | Gestion des User Stories (US01 à US07) et du flux de travail. |
| **Planification** | GanttProject (.gan) | Planification des tâches $\le$ 2 jours avec affectation des ressources. |
| **Modélisation** | Looping (.mdc) | Schéma Entité-Association (MCD Merise). |

---

## 3. Flux d'Interactions Principaux

### A. Inscription et Connexion Sécurisée
1. Saisie des identifiants dans le terminal (`cli.py`).
2. Vérification d'unicité et politique de mot de passe dans `AuthService`.
3. Génération d'un sel cryptographique et calcul du hachage SHA-256 (`security.py`).
4. Écriture atomique dans `data/users.json` via `StorageService`.

### B. Création Manuelle d'un Quiz (Sprint 3 - US04)
1. L'administrateur renseigne le titre et la description.
2. Ajout itératif de questions QCM avec plusieurs choix et indication de la bonne réponse.
3. Sérialisation de l'arborescence (`Quiz` $\rightarrow$ `Question` $\rightarrow$ `Reponse`) dans `data/quizzes.json`.

### C. Importation via Fichier Texte (Sprint 3 - US05)
1. L'administrateur charge un fichier texte structuré (`sample_quiz.txt`).
2. Le parseur extrait les balises `TITRE:`, `QUESTION:`, `*` (bonne réponse), `-` (fausses réponses).
3. Contrôle de validité et intégration automatique dans `data/quizzes.json`.

### D. Passation d'un Quiz par un Joueur (Sprint 3 - US06)
1. Sélection d'un quiz dans le catalogue.
2. Déroulement question par question avec validation des saisies.
3. Calcul en temps réel du score et restitution du corrigé pédagogique.
