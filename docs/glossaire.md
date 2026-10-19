# Glossaire du Projet Quiz Python (PROJ531)

Ce glossaire définit les termes méthodologiques et techniques utilisés tout au long du projet afin de garantir une terminologie commune entre les membres de l'équipe et le commanditaire (enseignant).

---

## 1. Termes de Gestion de Projet & Méthode Agile

- **Agile / Scrum :** Méthodologie itérative et incrémentale de gestion de projet privilégiant les cycles courts, l'adaptation continue et la livraison régulière de fonctionnalités opérationnelles.
- **Sprint :** Période délimitée dans le temps (ici 2 à 5 jours selon la planification) au cours de laquelle l'équipe conçoit, développe et teste un ensemble précis de fonctionnalités.
- **Product Owner (PO) :** Membre de l'équipe (Bilal Draoui) faisant l'interface avec le commanditaire, garant de la vision du produit, de la priorisation du backlog et de l'atteinte des objectifs.
- **WBS (Work Breakdown Structure / Organigramme des Tâches) :** Décomposition hiérarchique orientée livrables de l'ensemble des travaux nécessaires à la réalisation du projet.
- **Diagramme de Gantt :** Outil graphique de planification temporelle reliant les tâches, leurs dépendances, leurs durées prévisionnelles et les jalons (milestones) des sprints.
- **Backlog :** Liste ordonnée de toutes les fonctionnalités, exigences et correctifs attendus pour le produit.
- **Kanban (Trello) :** Outil visuel de gestion du flux de travail découpé en colonnes (*À faire*, *En cours*, *En revue*, *Terminé*) permettant de suivre la progression et l'affectation des tâches.

---

## 2. Termes de Conception & Modélisation

- **MCD (Modèle Conceptuel de Données) :** Représentation graphique formelle (formalisme Entité-Association / Merise) structurant l'information du système indépendamment de toute considération technique de stockage.
- **Entité :** Objet ou concept identifiable du domaine métier (ex. `Utilisateur`, `Quiz`, `Question`, `Reponse`, `Resultat`).
- **Cardinalité :** Nombre minimum et maximum de fois où une entité peut participer à une relation (ex. `1,1` : au moins une et au plus une ; `0,n` : zéro à plusieurs).
- **Attribut / Propriété :** Caractéristique élémentaire d'une entité (ex. `pseudo`, `email`, `score`).

---

## 3. Termes Techniques & Développement Python

- **CLI (Command-Line Interface) :** Interface utilisateur en ligne de commande permettant d'interagir avec l'application via le terminal texte.
- **JSON (JavaScript Object Notation) :** Format textuel léger et standardisé d'échange et de stockage de données structurées sous forme de paires clé/valeur et de listes.
- **Hachage cryptographique (SHA-256) :** Algorithme mathématique unidirectionnel transformant une chaîne de caractères (comme un mot de passe) en une empreinte de taille fixe de 64 caractères hexadécimaux, impossible à inverser.
- **Sel (Salt) :** Donnée aléatoire générée cryptographiquement concaténée au mot de passe avant son hachage, empêchant les attaques par dictionnaires et tables arc-en-ciel (*rainbow tables*).
- **Architecture en Couches (Layered Architecture) :** Organisation logicielle séparant le modèle de données (`models/`), la logique métier (`services/`), les utilitaires transverses (`utils/`) et l'interface utilisateur (`main.py`).
- **Tests unitaires (`unittest`) :** Procédure de validation automatisée vérifiant le bon fonctionnement d'un module ou d'une fonction isolée pour détecter immédiatement les régressions et les bugs.
