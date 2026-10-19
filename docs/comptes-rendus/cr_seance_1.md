# Compte-Rendu de Séance n°1 - Cadrage et Conception initiale
**Date :** Mardi 13 Octobre 2026  
**Module :** PROJ531 - Gestion de projet informatique  
**Équipe :** Groupe Quiz Python (4 membres)  
- **Product Owner :** Bilal Draoui  
- **Développeurs / Collaborateurs :** Sabrine Kawiche, Chadi Kharchoufa, Gabrien Vaz  

---

## 1. Objectifs de la séance
L'objectif de cette première séance était d'effectuer le cadrage complet du projet, de définir l'architecture globale, d'initialiser les outils de gestion de projet (Scrum, Trello, Git) et de concevoir le Modèle Conceptuel de Données (MCD).

---

## 2. Tâches réalisées lors de la séance

| Tâche WBS / Gantt | Responsable | Description | Temps estimé | Temps réel | Statut |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **1.1 Initialisation Git & README** | Bilal Draoui & Sabrine Kawiche | Création du dépôt GitHub, configuration des accès pour l'équipe, premier fichier README. | 1h30 | 1h15 | **Terminé** |
| **1.2 Conception du MCD** | Sabrine Kawiche & Bilal Draoui | Modélisation Entité-Association sur Looping (`quiz.mdc`) : Utilisateur, Quiz, Question, Réponse, Résultat. | 2h00 | 2h30 | **Terminé** |
| **1.3 Découpage WBS & Planning Gantt** | Chadi Kharchoufa | Élaboration du WBS (4 axes) et planification des 4 sprints sur GanttProject (`Gantt_projet_quiz.gan`). | 2h00 | 2h15 | **Terminé** |
| **1.4 Configuration Trello** | Gabrien Vaz & Équipe | Création du tableau Kanban avec colonnes Backlog, À faire, En cours, En revue, Terminé. | 1h00 | 0h45 | **Terminé** |

---

## 3. Tâches restantes et reportées au Sprint 2
- Mise en place de la structure de code Python (arborescence `src/`, `models/`, `services/`, `data/`).
- Implémentation du système d'authentification (Sprint 2 - Tâche 2.1).
- Conception du mécanisme de sérialisation JSON (Sprint 2 - Tâche 2.2).

---

## 4. Difficultés rencontrées et solutions apportées
1. **Périmètre du MCD :**
   - *Difficulté :* Hésitation sur le fait de lier les réponses de chaque utilisateur question par question ou seulement enregistrer le score final.
   - *Solution :* Conformément au cahier des charges qui demande au minimum *« de conserver l'historique des scores individuels à différents quizz »*, nous avons lié l'entité `Résultat` à `Utilisateur` et `Quiz`.
2. **Découpage des sprints :**
   - *Difficulté :* Respecter la règle SCRUM des tâches n'excédant pas 2 journées.
   - *Solution :* Décomposition fine en 4 sprints clairs et progressifs (Cadrage $\rightarrow$ Auth/Stockage $\rightarrow$ Moteur Quiz $\rightarrow$ Scores & Finalisation).

---

## 5. Prochaine séance (Séance 2 - 19/10/2026)
- Démarrage effectif du **Sprint 2 : Authentification et Stockage JSON**.
- Écriture des modèles de données et du service de gestion des utilisateurs (connexion, inscription, hachage sécurisé des mots de passe).
