# Compte-Rendu de Séance n°5 - Finalisation, Rapport final & Préparation de la soutenance
**Date :** Lundi 09 Novembre 2026  
**Module :** PROJ531 - Gestion de projet informatique  
**Équipe :** Groupe Quizora (4 membres)  
- **Product Owner :** Bilal Draoui  
- **Développeurs / Collaborateurs :** Sabrine Kawiche, Chadi Kharchoufa, Gabrien Vaz  

**Statut du sprint :** **Sprint 4 - Prolongation (Rapport final & Soutenance en cours)**

---

## 1. Objectifs de la Séance n°5
Le planning initial (Gantt et README) prévoyait 4 sprints se terminant le 06/11/2026. Toutes les fonctionnalités sont livrées. En séance 4, l'équipe a établi le plan du rapport final et le scénario de la démonstration ; il reste à rédiger entièrement le rapport et à répéter la soutenance. La séance 5 est donc consacrée à la finalisation du projet :

1. **Préparation de la soutenance :** révision des notions de gestion de projet et de Git/GitHub, simulation des questions de l'enseignant, préparation de la démonstration de 15 minutes.
2. **Rapport final :** rédaction du rapport de fin de projet demandé par le sujet.
3. **Nettoyage du dépôt GitHub :** ne conserver que la branche principale à jour et vérifier que la version livrée fonctionne sans bug.
4. **Suivi de projet :** compléter les temps réels du CR4 et déposer le présent compte rendu.

---

## 2. Travail livré entre la séance 4 et la séance 5
Le 02/11/2026, après la séance 4, deux évolutions ont été intégrées sur la branche `main` :

- **Quiz de démonstration :** trois quiz d'exemple (dossier `exemples/` : *Les bases de Python*, *Gestion de projet et méthode Scrum*, *Culture générale*, 5 questions chacun) sont importés automatiquement au premier lancement, au nom du compte `admin`. L'application peut ainsi être testée immédiatement après un `git clone`, sans saisie préalable. Deux tests unitaires vérifient cet import.
- **Interface graphique complète :** la GUI Tkinter permet désormais à l'administrateur de créer un quiz et d'importer un fichier `.txt`, et au joueur de passer un quiz (bouton « Jouer ») puis de consulter son historique de scores. Les deux modes (console et graphique) offrent donc les mêmes fonctionnalités.

---

## 3. Répartition des tâches de la séance

| Tâche | Responsable | Description | Temps estimé | Temps réel | Statut |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Nettoyage du dépôt GitHub** | Bilal Draoui | Fermeture de la Pull Request #1 et suppression de la branche `gabv1138-coder-patch-1`, dont le contenu (passation de quiz) était déjà intégré dans `main`. | 0h15 | ~0h15 | **En cours** |
| **Vérification de la version livrée** | Bilal Draoui | Exécution de la suite de tests unitaires sur `main`. | 0h15 | ~0h10 | **En cours** |
| **Soutenance : répétition** | Équipe | Révision des notions Git/GitHub (commandes du quotidien, conflits, branches, `.gitignore`), simulation des questions de l'enseignant, répétition chronométrée de la démonstration préparée en séance 4. | 1h30 | ~1h00 | **En cours** |
| **Rapport final : rédaction complète** | Bilal Draoui & Équipe | Rédaction du rapport (`docs/rapport_final.md` et version PDF) à partir du plan établi en séance 4, puis relecture par l'équipe. | 3h00 | ~2h30 | **En cours** |
| **Compléter les temps réels du CR4** | Équipe | Chaque responsable renseigne le temps réellement passé sur ses tâches du Sprint 4. | 0h15 | ~0h15 | **En cours** |

> Temps réels approximatifs (~), estimés a posteriori par l'équipe.

---

## 4. Choix et décisions de la séance

1. **Une seule branche sur le dépôt :**
   - *Constat :* une Pull Request ouverte depuis le 23/10 (branche `gabv1138-coder-patch-1`, créée lors d'une modification directe de `cli.py` sur le site GitHub) restait en attente, alors que son contenu avait déjà été intégré dans `main`.
   - *Décision :* fermer la Pull Request et supprimer la branche. Le commit reste consultable dans la Pull Request fermée ; aucun travail n'est perdu.
2. **Retour d'expérience sur l'utilisation de Git :**
   - *Constat :* l'équipe a travaillé principalement directement sur `main`, ce qui a provoqué un conflit sur `src/cli.py` lors de la séance 4.
   - *Décision :* présenter ce point dans le rapport final comme piste d'amélioration (une branche par user story et une Pull Request relue par un autre membre).

---

## 5. Vérifications
- La suite complète de tests unitaires passe sur la branche `main` :
  ```bash
  python -m unittest discover tests
  # Ran 30 tests ... OK
  ```
- Le dépôt ne contient plus qu'une seule branche (`main`) et aucune Pull Request ouverte.

---

## 6. Difficultés rencontrées
- **Dépassement du planning :** le Gantt prévoyait la fin du projet le 06/11/2026. Le plan du rapport et le scénario de démonstration ont bien été préparés en séance 4, mais la rédaction complète du rapport et la répétition de la soutenance se poursuivent en séance 5, car le développement a pris plus de temps que prévu en fin de Sprint 4 (historique des scores, corrections de bugs, interface graphique).

---

## 7. Suivi de projet & Organisation Kanban (Trello)
- Les cartes de la séance 5 ont été créées sur le tableau : **T05.1** Nettoyage du dépôt GitHub, **T05.2** Vérification de la version livrée, **T05.3** Soutenance : répétition, **T05.4** Rapport final : rédaction complète, **T05.5** Compléter les temps réels du compte rendu 4 (colonne **À faire (Sprint actuel)**).
- La carte **Chasse aux bugs et robustesse** (Chadi Kharchoufa, Sabrine Kawiche) est dans la colonne **En cours**.
- La colonne **Terminé** regroupe 31 cartes des sprints précédents.

Ci-dessous, la capture d'écran du tableau Trello à la fin de la séance 5 :

![Tableau Trello - Séance 5](../trello_sprint5.png)

---

## 8. Prochaines étapes
- Faire relire le **rapport final** (`docs/rapport_final.md`) par toute l'équipe et y apporter les dernières corrections.
- **Répéter la démonstration** en respectant les 15 minutes : connexion admin, création ou import d'un quiz, connexion joueur, passation d'un quiz, consultation de l'historique, en console puis en interface graphique.
- Renseigner les **temps réels** dans les CR4 et CR5.
- Préparer l'**évaluation par les pairs** demandée par l'enseignant.
