# Compte-Rendu de Séance n°4 - Sprint 4 (Historique des scores, Consolidation & Soutenance)
**Date :** Lundi 02 Novembre 2026  
**Module :** PROJ531 - Gestion de projet informatique  
**Équipe :** Groupe Quizora (4 membres)  
- **Product Owner :** Bilal Draoui  
- **Développeurs / Collaborateurs :** Sabrine Kawiche, Chadi Kharchoufa, Gabrien Vaz  

**Statut du sprint :** **Sprint 4 - Finitions & Soutenance (En cours)**

---

## 1. Objectifs de la Séance n°4 (Sprint 4)
Le Sprint 3 a livré le cœur du jeu (création, import et passation de quiz). Entre-temps, une interface graphique Tkinter (page de connexion et tableau de bord) a été ajoutée et le dossier d'architecture technique a été mis à jour. Le Sprint 4, dernier sprint du projet, a pour objectifs :

1. **Historique des scores (US07 / Tâche 3.4) :** Enregistrer chaque passage de quiz dans `data/results.json` et permettre au joueur de consulter son historique personnel.
2. **Chasse aux bugs (Tâche 4.1) :** Relire le code livré aux sprints précédents, repérer et corriger les anomalies.
3. **Rapport final (Tâche 4.2) :** Rédiger le rapport de fin de projet.
4. **Préparation de la soutenance (Tâche 4.3) :** Préparer et répéter la démonstration orale de 15 minutes.

---

## 2. Répartition des tâches WBS / Gantt de la séance

| Tâche WBS / Gantt | Responsable | Description | Temps estimé | Statut |
| :--- | :--- | :--- | :---: | :---: |
| **3.4 Joueur : Sauvegarde et historique des scores (US07)** | Sabrine Kawiche & Bilal Draoui | Enregistrement du score dans `data/results.json` à la fin d'un quiz et affichage de l'historique du joueur dans le menu console. | 2h00 | **En cours** |
| **3.4.bis Tests unitaires de l'historique** | Gabrien Vaz | Tests automatisés de la sauvegarde des résultats et de l'historique. | 1h00 | **À faire** |
| **4.1 Chasse aux bugs et robustesse** | Chadi Kharchoufa & Sabrine Kawiche | Relecture du parseur d'import et du parcours joueur, correction des anomalies relevées (voir section 3.2). | 1h30 | **En cours** |
| **4.2 Rédaction du rapport final** | Bilal Draoui & Équipe | Synthèse du projet : gestion de projet (WBS, PBS, Gantt, Trello), architecture, bilan des sprints. | 2h00 | **En cours** |
| **4.3 Préparation de la soutenance** | Équipe | Scénario de démonstration (admin puis joueur), support de présentation, répétition chronométrée. | 1h30 | **À faire** |

---

## 3. Travail réalisé pendant la séance

### 3.1 Historique des scores (US07)
- **Sauvegarde du score (Sabrine Kawiche) :** à la fin de `action_passer_quiz`, un objet `Resultat` (joueur, quiz, score, score maximal, date) est créé et ajouté à `data/results.json` grâce aux méthodes `load_results()` / `save_results()` du `StorageService`, prévues depuis le Sprint 2. Le message « Votre score a été enregistré ! » confirme la sauvegarde.
- **Consultation de l'historique :** l'option 3 de l'espace joueur, qui affichait jusqu'ici « sera intégré lors du Sprint 4 », appelle désormais la méthode `action_consulter_historique`. Celle-ci affiche, pour le joueur connecté, la date, le titre du quiz et le score obtenu :
  ```text
  --- HISTORIQUE DE JOUEUR1 ---
  2026-11-02 | Culture Informatique et Génie Logiciel | 4/4 (100.0%)
  2026-11-02 | Culture Informatique et Génie Logiciel | 3/4 (75.0%)
  ```
- **Correctif :** dans la première version, la méthode `action_consulter_historique` était appelée par le menu mais n'existait pas encore, ce qui faisait planter l'application (`AttributeError`) dès qu'un joueur choisissait l'option 3. La méthode a été ajoutée et le parcours fonctionne de bout en bout.

### 3.2 Chasse aux bugs (Tâche 4.1) - anomalies relevées
| Anomalie constatée | Cause | Statut |
| :--- | :--- | :---: |
| L'option 3 « Consulter mon historique de scores » faisait planter l'application. | Méthode `action_consulter_historique` appelée mais pas encore écrite. | **Corrigé** |
| Une question importée avec le barème `[1 pt]` garde le texte « [1 pt] » dans son énoncé (cas présent dans `sample_quiz.txt`). | Le parseur d'import ne reconnaît que la forme plurielle `pts]`. | **À corriger** |
| Les tests du parseur d'import ne sont pas lancés par `python -m unittest discover tests`. | Le fichier `test_import.py` se trouve à la racine du dépôt et non dans `tests/`. | **À corriger** |
| Un quiz sans aucune question peut être lancé et produit un score « 0 / 0 ». | Aucune vérification avant le démarrage du quiz. | **À corriger** |

### 3.3 Vérifications
- La suite de tests existante (19 tests) passe toujours :
  ```bash
  python -m unittest discover tests
  # Ran 19 tests ... OK
  ```
- Parcours rejoué en console : connexion `admin`, import de `sample_quiz.txt`, connexion `joueur1`, deux passages du quiz (4/4 puis 3/4), puis consultation de l'historique.

---

## 4. Suivi de projet & Organisation Kanban (Trello)
- Le **PBS** (Product Breakdown Structure) du projet a été ajouté dans `docs/PBS_Quizora.png`.
- Les cartes **US07** (historique des scores), **T3.4** et **T4.1** (chasse aux bugs) sont dans la colonne **En cours**.
- Les cartes **T3.4.bis** (tests de l'historique), **T4.2** (rapport final) et **T4.3** (soutenance) sont dans les colonnes **À faire** / **En cours** jusqu'à la fin du sprint.
- *Capture du tableau Trello à ajouter en fin de sprint : `docs/trello_sprint4.png`.*

---

## 5. Points restant à traiter avant la soutenance
- **Corrections (4.1) :** traiter les trois anomalies « À corriger » de la section 3.2.
- **Tests (3.4.bis) :** ajouter les tests unitaires de la sauvegarde et de l'historique des scores.
- **Interface graphique :** le tableau de bord Tkinter liste les quiz mais ne permet pas encore de les passer ni d'afficher l'historique ; la démonstration de ces fonctionnalités se fera donc en mode console. À décider en équipe : intégrer l'historique dans la GUI ou le présenter comme une évolution possible.
- **Rapport final (4.2) :** reprendre les quatre comptes-rendus, le WBS, le PBS, le Gantt, le MCD et le dossier d'architecture technique.
- **Soutenance (4.3) :** préparer un jeu de données de démonstration propre (quiz importé + quelques résultats) et répéter la démonstration en respectant les 15 minutes.

---

## 6. Bilan global du projet
| Sprint | Contenu livré | Statut |
| :--- | :--- | :---: |
| Sprint 1 | Cadrage, WBS, Gantt, MCD, tableau Trello | Terminé |
| Sprint 2 | Architecture modulaire, comptes sécurisés (SHA-256 salé), stockage JSON, menu console | Terminé |
| Sprint 3 | Création manuelle et import de quiz, passation et calcul du score, interface graphique de connexion | Terminé |
| Sprint 4 | Historique des scores, corrections de bugs, rapport final et soutenance | En cours |

Les user stories US01 à US06 sont terminées. L'US07 (historique des scores) est fonctionnelle et en cours de finalisation (tests et corrections). Il reste ensuite les livrables de fin de projet (rapport et soutenance).
