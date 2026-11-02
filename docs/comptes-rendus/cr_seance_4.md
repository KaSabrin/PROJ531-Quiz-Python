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
2. **Chasse aux bugs (Tâche 4.1) :** Relire le code livré aux sprints précédents, corriger les anomalies et vérifier que tous les tests sont réellement exécutés.
3. **Rapport final (Tâche 4.2) :** Rédiger le rapport de fin de projet.
4. **Préparation de la soutenance (Tâche 4.3) :** Préparer et répéter la démonstration orale de 15 minutes.

---

## 2. Répartition des tâches WBS / Gantt de la séance

| Tâche WBS / Gantt | Responsable | Description | Temps estimé | Statut |
| :--- | :--- | :--- | :---: | :---: |
| **3.4 Joueur : Sauvegarde et historique des scores (US07)** | Sabrine Kawiche & Bilal Draoui | Sauvegarde du score en fin de quiz (Sabrine), puis regroupement dans le service `ResultatService`, enregistrement automatique du score en fin de quiz, menu « Consulter mon historique de scores » dans le CLI. | 2h00 | **Terminé** |
| **3.4.bis Tests unitaires de l'historique** | Gabrien Vaz | Nouveau fichier `tests/test_resultat.py` (5 tests) : persistance, rejet des scores incohérents, filtrage par joueur, statistiques. | 1h00 | **Terminé** |
| **4.1 Chasse aux bugs et robustesse** | Chadi Kharchoufa & Sabrine Kawiche | Relecture du parseur d'import et du parcours joueur, corrections et tests de non-régression. | 1h30 | **Terminé** |
| **4.2 Rédaction du rapport final** | Bilal Draoui & Équipe | Synthèse du projet : gestion de projet (WBS, Gantt, Trello), architecture, bilan des sprints. | 2h00 | **En cours** |
| **4.3 Préparation de la soutenance** | Équipe | Scénario de démonstration (admin puis joueur), support de présentation, répétition chronométrée. | 1h30 | **À faire** |

---

## 3. Travail réalisé pendant la séance

### 3.1 Historique des scores (US07)
- **Première version (Sabrine Kawiche) :** enregistrement du résultat dans `data/results.json` directement à la fin de `action_passer_quiz`, et branchement de l'option 3 du menu joueur sur une méthode `action_consulter_historique`.
- **Nouveau service `src/services/resultat_service.py`** (`ResultatService`), qui s'appuie sur le modèle `Resultat` et les méthodes `load_results()` / `save_results()` du `StorageService`, déjà prévues depuis le Sprint 2 mais encore inutilisées :
  - `enregistrer_resultat(joueur, quiz, score)` : crée un `Resultat` (score, score maximal, date de passage) et l'ajoute à `data/results.json`. Un score négatif ou supérieur au barème du quiz est refusé.
  - `historique_joueur(joueur)` : renvoie uniquement les résultats du joueur connecté, du plus récent au plus ancien.
  - `statistiques_joueur(joueur)` : nombre de quiz passés, moyenne et meilleur pourcentage.
- **Intégration dans le CLI (`src/cli.py`) :**
  - À la fin d'un quiz, le score est sauvegardé automatiquement et un message de confirmation s'affiche.
  - L'option 3 de l'espace joueur, qui affichait jusqu'ici « sera intégré lors du Sprint 4 », ouvre désormais l'historique :
    ```text
    HISTORIQUE DES SCORES DE JOUEUR1
    ======================================================================
    Date               Quiz                                 Score        %
    ----------------------------------------------------------------------
    2026-11-02 15:06   Culture Informatique et Génie L        4/4   100.0%
    2026-11-02 15:06   Culture Informatique et Génie L        3/4    75.0%
    ----------------------------------------------------------------------
    Quiz passés : 2 | Moyenne : 87.5% | Meilleur score : 100.0%
    ```
  - Si un quiz a été supprimé entre-temps, la ligne de l'historique affiche « (quiz supprimé) » au lieu de planter.

### 3.2 Chasse aux bugs (Tâche 4.1)
| Anomalie constatée | Cause | Correction |
| :--- | :--- | :--- |
| Une question importée avec le barème `[1 pt]` gardait le texte « [1 pt] » dans son énoncé (cas présent dans `sample_quiz.txt`). | Le parseur ne reconnaissait que la forme plurielle `pts]`. | Lecture du barème par expression régulière, qui accepte `[1 pt]` comme `[2 pts]`. Test de non-régression `test_bareme_singulier_pt` ajouté. |
| Les tests du parseur d'import n'étaient jamais lancés par `python -m unittest discover tests`. | Le fichier `test_import.py` se trouvait à la racine du dépôt au lieu du dossier `tests/`. | Fichier déplacé dans `tests/test_import.py`. |
| L'option 3 « Consulter mon historique de scores » faisait planter l'application (`AttributeError`). | La méthode `action_consulter_historique` était appelée dans le menu joueur mais n'avait pas encore été écrite. | Méthode implémentée à partir du `ResultatService` ; l'enregistrement du score passe désormais uniquement par ce service pour éviter une double sauvegarde. |
| Un quiz sans aucune question pouvait être lancé et produire un score « 0 / 0 ». | Aucune vérification avant le démarrage du quiz. | Le CLI refuse désormais de lancer un quiz vide avec un message explicite. |

### 3.3 Assurance qualité
- La suite de tests passe de **19 à 27 tests**, tous validés :
  ```bash
  python -m unittest discover tests
  # Ran 27 tests ... OK
  ```
- Un parcours complet a été rejoué en console : connexion `admin`, import de `sample_quiz.txt`, déconnexion, connexion `joueur1`, deux passages du quiz (4/4 puis 3/4), puis consultation de l'historique (moyenne 87,5 %, meilleur score 100 %).

---

## 4. Suivi de projet & Organisation Kanban (Trello)
- Le **PBS** (Product Breakdown Structure) du projet a été ajouté dans `docs/PBS_Quizora.png`.
- Les cartes **US07** (historique des scores), **T3.4** et **T4.1** (chasse aux bugs) sont déplacées dans la colonne **Terminé**.
- Les cartes **T4.2** (rapport final) et **T4.3** (soutenance) restent dans la colonne **En cours** / **À faire** jusqu'à la fin du sprint.
- *Capture du tableau Trello à ajouter en fin de sprint : `docs/trello_sprint4.png`.*

---

## 5. Points restant à traiter avant la soutenance
- **Interface graphique :** le tableau de bord Tkinter liste les quiz mais ne permet pas encore de les passer ni d'afficher l'historique ; la démonstration de ces fonctionnalités se fera donc en mode console. À décider en équipe : intégrer l'historique dans la GUI ou le présenter comme une évolution possible.
- **Rapport final (4.2) :** reprendre les quatre comptes-rendus, le WBS, le Gantt, le MCD et le dossier d'architecture technique.
- **Soutenance (4.3) :** préparer un jeu de données de démonstration propre (quiz importé + quelques résultats) et répéter la démonstration en respectant les 15 minutes.

---

## 6. Bilan global du projet (à l'issue des 4 sprints)
| Sprint | Contenu livré | Statut |
| :--- | :--- | :---: |
| Sprint 1 | Cadrage, WBS, Gantt, MCD, tableau Trello | Terminé |
| Sprint 2 | Architecture modulaire, comptes sécurisés (SHA-256 salé), stockage JSON, menu console | Terminé |
| Sprint 3 | Création manuelle et import de quiz, passation et calcul du score, interface graphique de connexion | Terminé |
| Sprint 4 | Historique des scores, corrections de bugs, rapport final et soutenance | En cours |

Toutes les user stories fonctionnelles prévues au backlog (US01 à US07) sont désormais implémentées. Il reste uniquement les livrables de fin de projet (rapport et soutenance).
