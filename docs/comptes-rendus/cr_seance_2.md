# Compte-Rendu de Séance n°2 - Lancement du Sprint 2 (Authentification & Stockage)
**Date :** Lundi 19 Octobre 2026  
**Module :** PROJ531 - Gestion de projet informatique  
**Équipe :** Groupe Quizora (4 membres)  
- **Product Owner :** Bilal Draoui  
- **Développeurs / Collaborateurs :** Sabrine Kawiche, Chadi Kharchoufa, Gabrien Vaz  

**Statut du sprint :** 🟡 **En cours** (Sprint 2 : du 19/10 au 22/10)

---

## 1. Objectifs du Sprint 2
Conformément au WBS (lot 2) et au diagramme de Gantt, le Sprint 2 vise à :
- Structurer l'architecture logicielle modulaire (`src/models`, `src/services`, `src/utils`).
- Mettre en place la persistance JSON des utilisateurs (`data/users.json`).
- Gérer les comptes utilisateurs de façon sécurisée (inscription, connexion, hachage des mots de passe, distinction Joueur / Admin).
- Écrire des tests unitaires pour livrer une version sans bug en fin de sprint.

---

## 2. Avancement des tâches

| Tâche WBS / Gantt | Responsable | Description | Temps estimé | Temps réel | Statut |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **2.0 Architecture & structure du code** | Bilal Draoui & Équipe | Arborescence `src/` (models, services, utils) et `tests/`, point d'entrée unique `main.py`. | 1h00 | 0h45 | 🟢 **Terminé** |
| **2.1.bis Sécurité des mots de passe** | Chadi Kharchoufa & Bilal Draoui | Hachage SHA-256 avec sel aléatoire (`src/security.py`) et tests unitaires (`test_security.py`). | 1h30 | 1h15 | 🟢 **Terminé** |
| **2.1 Gestion des utilisateurs (inscription / connexion)** | Sabrine Kawiche & Bilal Draoui | Modèle `User` initialisé, service `AuthService`, validation des entrées et gestion des rôles. | 2h30 | 2h00 | 🟡 En cours |
| **2.2 Stockage des données (JSON)** | Gabrien Vaz | Service `StorageService` : lecture/écriture JSON, gestion automatique du dossier `data/`. | 1h30 | 1h15 | 🟡 En cours |
| **2.3 Menu console (CLI)** | Sabrine Kawiche & Équipe | Menus d'inscription, de connexion et espaces Joueur / Admin dans `src/cli.py`. | 1h30 | 1h00 | 🟡 En cours |
| **2.4 Tests unitaires automatisés** | Gabrien Vaz & Bilal Draoui | Tests de la sécurité validés (4/4 tests OK sur Git), tests auth et stockage en finalisation. | 1h30 | 1h00 | 🟡 En cours |

> Le code du Sprint 2 est en cours de développement et sera poussé sur GitHub une fois relu et testé par l'équipe.

---

## 3. Choix techniques décidés pendant la séance
1. **Stockage sécurisé des mots de passe :**
   - *Constat :* Le MCD initial prévoyait un attribut `mdp`. Stocker les mots de passe en clair dans un fichier JSON serait une faille de sécurité.
   - *Décision :* Renommer le champ en `mdp_hash` et stocker un hachage SHA-256 salé au format `sel$hash`.
2. **Encodage des fichiers JSON :**
   - *Constat :* Risque de mauvais affichage des caractères accentués sous Windows.
   - *Décision :* Lire et écrire systématiquement en `utf-8` avec `ensure_ascii=False`.
3. **Point d'entrée unique :**
   - *Décision :* Conserver le `main.py` à la racine du dépôt (créé lors de l'initialisation du projet) comme unique point d'entrée ; le menu est placé dans `src/cli.py`.
4. **Données locales non versionnées :**
   - *Décision :* Le dossier `data/` est exclu de Git (`.gitignore`) pour ne pas publier les comptes utilisateurs ; il est recréé automatiquement au lancement.

---

## 4. Prochaine séance
- Terminer et tester les tâches 2.0 à 2.4, puis pousser le code du Sprint 2 sur GitHub.
- Démarrer le Sprint 3 (26/10) : création manuelle de quiz (3.1), import depuis un fichier texte (3.2), passation d'un quiz par un joueur (3.3).
