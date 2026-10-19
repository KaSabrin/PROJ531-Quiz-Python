# Compte-Rendu de Séance n°2 - Lancement du Sprint 2 (Authentification & Stockage)
**Date :** Lundi 19 Octobre 2026  
**Module :** PROJ531 - Gestion de projet informatique  
**Équipe :** Groupe Quiz Python (4 membres)  
- **Product Owner :** Bilal Draoui  
- **Développeurs / Collaborateurs :** Sabrine Kawiche, Chadi Kharchoufa, Gabrien Vaz  

---

## 1. Objectifs de la séance
L'objectif de cette deuxième séance est le développement du **Sprint 2 : Authentification et Stockage des données**, conformément au WBS (lot 2) et au diagramme de Gantt :
- Structuration de l'architecture logicielle modulaire (`src/models`, `src/services`, `src/utils`).
- Implémentation de la persistance JSON pour les utilisateurs (`data/users.json`).
- Gestion sécurisée des comptes utilisateurs (inscription, connexion, hachage SHA-256 avec sel, distinction Joueur / Admin).
- Écriture d'une suite de tests unitaires pour garantir un code sans bug (« version propre » exigée par le sujet).

---

## 2. Tâches réalisées lors de la séance

| Tâche WBS / Gantt | Responsable | Description | Temps estimé | Temps réel | Statut |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **2.0 Architecture modulaire & structure** | Bilal Draoui & Équipe | Mise en place de l'arborescence standardisée (`src/`, `data/`, `tests/`), configuration `.gitignore`. | 1h00 | 0h45 | **Terminé** |
| **2.1 Gestion des utilisateurs (Auth)** | Bilal Draoui & Sabrine Kawiche | Création du modèle `User`, du service `AuthService`, validation des entrées (email, pseudo) et gestion des rôles. | 2h30 | 2h15 | **Terminé** |
| **2.1.bis Sécurité & Hachage des MDP** | Chadi Kharchoufa | Module `security.py` : hachage cryptographique SHA-256 avec sel aléatoire (`secrets.token_hex`) et comparaison à temps constant. | 1h30 | 1h15 | **Terminé** |
| **2.2 Stockage JSON (StorageService)** | Gabrien Vaz | Module `storage_service.py` : sérialisation/désérialisation JSON, création automatique des répertoires et fichiers par défaut. | 1h30 | 1h30 | **Terminé** |
| **2.3 Interface CLI d'authentification** | Sabrine Kawiche & Bilal Draoui | Menu console ergonomique permettant l'inscription, la connexion et l'accès aux espaces Joueur / Admin. | 1h30 | 1h15 | **Terminé** |
| **2.4 Tests unitaires automatisés** | Gabrien Vaz & Chadi Kharchoufa | Suite de tests dans `tests/test_auth.py` et `tests/test_storage.py` validant tous les cas nominaux et d'erreur. | 1h30 | 1h30 | **Terminé** |

---

## 3. Tâches restantes pour la prochaine séance (Séance 3 - Sprint 3)
- Création manuelle de quiz par l'administrateur (Tâche 3.1).
- Importation de quiz via un fichier texte structuré (Tâche 3.2).
- Moteur de passation de quiz pour les joueurs autorisés (Tâche 3.3).

---

## 4. Difficultés rencontrées et solutions apportées
1. **Stockage sécurisé des mots de passe :**
   - *Difficulté :* Le MCD initial mentionnait un attribut `mdp`. Stocker les mots de passe en clair dans un fichier JSON constitue une faille de sécurité majeure.
   - *Solution :* Adoption d'une fonction de hachage SHA-256 salée avec `salt$hash` stocké dans `mdp_hash`. Un mot de passe volé ne peut ainsi pas être inversé ni attaqué par tables arc-en-ciel.
2. **Encodage et persistance JSON sous Windows :**
   - *Difficulté :* Gestion des caractères accentués français dans les fichiers JSON.
   - *Solution :* Forcer systématiquement l'encodage `utf-8` avec `ensure_ascii=False` dans le service de stockage.

---

## 5. Bilan technique de fin de séance
Le dépôt contient désormais une version fonctionnelle, testée et sans bug du système d'authentification et de persistance des données. Tous les tests unitaires passent avec succès (`Ran X tests in X.XXXs OK`).
