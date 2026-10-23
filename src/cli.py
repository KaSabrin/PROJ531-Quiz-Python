"""Interface utilisateur en ligne de commande (CLI) de l'application Quizora.

Ce module contient les menus. Le point d'entrée du programme est le fichier
main.py situé à la racine du dépôt.
"""

import getpass
import sys
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.storage_service import StorageService
from src.services.quiz_service import QuizService


def prompt_password(prompt: str = "Mot de passe : ") -> str:
    """Demande un mot de passe de manière sécurisée ou avec un fallback standard."""
    try:
        # getpass masque la saisie dans le terminal
        pwd = getpass.getpass(prompt)
        if pwd:
            return pwd
    except Exception:
        pass
    return input(prompt)


class QuizAppCLI:
    """Contrôleur de l'interface en ligne de commande de l'application."""

    def __init__(self):
        self.storage_service = StorageService()
        self.auth_service = AuthService(storage_service=self.storage_service)
        self.quiz_service = QuizService(storage_service=self.storage_service)

    def afficher_banniere(self) -> None:
        """Affiche le titre stylisé de l'application."""
        print("\n" + "=" * 60)
        print("                 QUIZORA - PROJ531 QUIZ PYTHON             ")
        print("=" * 60)

    def menu_principal(self) -> None:
        """Boucle du menu d'accueil avant authentification."""
        while True:
            self.afficher_banniere()
            print("1.  Se connecter")
            print("2.  S'inscrire (Nouveau compte)")
            print("3. ℹ  À propos & Comptes de démonstration")
            print("4.  Quitter")
            print("-" * 60)

            choix = input("Votre choix (1-4) : ").strip()

            if choix == "1":
                self.action_connexion()
            elif choix == "2":
                self.action_inscription()
            elif choix == "3":
                self.action_a_propos()
            elif choix == "4":
                print("\nMerci d'avoir utilisé Quizora. À bientôt !\n")
                sys.exit(0)
            else:
                print("\n Option invalide. Veuillez entrer un nombre entre 1 et 4.")

    def action_a_propos(self) -> None:
        """Affiche les informations du projet et les comptes de démo."""
        print("\n" + "-" * 50)
        print("ℹ  INFORMATIONS DU PROJET & COMPTES DE TEST")
        print("-" * 50)
        print("Application : Quizora")
        print("Projet : PROJ531 - Université Savoie Mont Blanc")
        print("Développement : Sprint 2 (Authentification & Stockage JSON)")
        print("\nComptes pré-configurés pour tester directement :")
        print("  • Administrateur :")
        print("      Identifiant : admin")
        print("      Mot de passe : Admin123!")
        print("  • Joueur :")
        print("      Identifiant : joueur1")
        print("      Mot de passe : Joueur123!")
        print("-" * 50)
        input("Appuyez sur [Entrée] pour revenir au menu...")

    def action_connexion(self) -> None:
        """Gère la saisie des identifiants et la connexion."""
        print("\n---  CONNEXION ---")
        identifiant = input("Pseudo ou Adresse e-mail : ").strip()
        mot_de_passe = prompt_password("Mot de passe : ")

        succes, message, user = self.auth_service.login(identifiant, mot_de_passe)

        if succes and user:
            print(f"\n {message}")
            if user.is_admin():
                self.menu_administrateur(user)
            else:
                self.menu_joueur(user)
        else:
            print(f"\n Erreur de connexion : {message}")
            input("Appuyez sur [Entrée] pour continuer...")

    def action_inscription(self) -> None:
        """Gère le formulaire d'inscription d'un nouvel utilisateur."""
        print("\n---  CRÉATION D'UN NOUVEAU COMPTE ---")
        pseudo = input("Choisissez un pseudo (3 à 30 car.) : ").strip()
        email = input("Votre adresse e-mail : ").strip()
        mot_de_passe = prompt_password("Mot de passe (min. 6 car., lettres + chiffres) : ")
        confirmation = prompt_password("Confirmez le mot de passe : ")

        if mot_de_passe != confirmation:
            print("\n Les deux mots de passe ne correspondent pas.")
            input("Appuyez sur [Entrée] pour continuer...")
            return

        succes, message, user = self.auth_service.register(
            pseudo=pseudo,
            email=email,
            password=mot_de_passe,
            role=User.ROLE_JOUEUR,
        )

        if succes and user:
            print(f"\n {message} Vous pouvez maintenant vous connecter.")
        else:
            print(f"\n Échec de l'inscription : {message}")

        input("Appuyez sur [Entrée] pour continuer...")

    def menu_joueur(self, user: User) -> None:
        """Menu interactif pour un utilisateur ayant le rôle 'joueur'."""
        while self.auth_service.is_authenticated():
            print("\n" + "=" * 50)
            print(f" ESPACE JOUEUR - Connecté : {user.pseudo}")
            print("=" * 50)
            print("1.  Voir mon profil")
            print("2.  Lister et passer un quiz (Sprint 3)")
            print("3.  Consulter mon historique de scores (Sprint 4)")
            print("4. Se déconnecter")
            print("-" * 50)

            choix = input("Votre choix (1-4) : ").strip()

            if choix == "1":
                self.afficher_profil(user)
            elif choix == "2":
                self.action_passer_quiz(user)
            elif choix == "3":
                print("\n[Sprint 4] L'historique détaillé des scores sera intégré lors du Sprint 4.")
                input("Appuyez sur [Entrée] pour continuer...")
            elif choix == "4":
                self.auth_service.logout()
                print("\nVous avez été déconnecté avec succès.")
                break
            else:
                print(" Choix invalide.")
    
    def action_passer_quiz(self, user: User) -> None:
        """Permet à un joueur de choisir et de passer un quiz interactif (Tâche 3.3)."""
        quizzes = self.quiz_service.lister_quiz()
        if not quizzes:
            print("\n⚠️ Aucun quiz n'est disponible pour le moment. Demandez à un administrateur d'en créer un.")
            input("Appuyez sur [Entrée] pour continuer...")
            return
        print("\n" + "=" * 55)
        print("🎯 CATALOGUE DES QUIZ DISPONIBLES")
        print("=" * 55)
        for idx, q in enumerate(quizzes, 1):
            print(f"{idx}. {q.titre} ({len(q.questions)} questions - {q.total_points()} points)")
            if q.description:
                print(f"   Description : {q.description}")
        print("-" * 55)
        choix = input(f"Choisissez un quiz (1-{len(quizzes)}) ou 'retour' : ").strip()
        if choix.lower() == "retour" or not choix.isdigit() or not (1 <= int(choix) <= len(quizzes)):
            return
        quiz = quizzes[int(choix) - 1]
        print("\n" + "=" * 55)
        print(f"🚀 DÉMARRAGE DU QUIZ : {quiz.titre.upper()}")
        print("=" * 55)
        score_obtenu = 0
        reponses_incorrectes = []
        for idx_q, question in enumerate(quiz.questions, 1):
            print(f"\nQuestion {idx_q}/{len(quiz.questions)} [{question.points} pt(s)] :")
            print(f"👉 {question.enonce}")
            for idx_r, rep in enumerate(question.reponses, 1):
                print(f"   {idx_r}. {rep.text_reponse}")
            # Saisie de la réponse du joueur
            while True:
                rep_joueur = input(f"Votre réponse (1-{len(question.reponses)}) : ").strip()
                if rep_joueur.isdigit() and 1 <= int(rep_joueur) <= len(question.reponses):
                    choix_idx = int(rep_joueur) - 1
                    break
                print("❌ Saisie invalide, entrez le numéro d'une des options.")
            if question.reponses[choix_idx].est_correct:
                print("✅ Bonne réponse !")
                score_obtenu += question.points
            else:
                bonnes = [r.text_reponse for r in question.get_bonnes_reponses()]
                print("❌ Mauvaise réponse.")
                reponses_incorrectes.append({
                    "question": question.enonce,
                    "choisie": question.reponses[choix_idx].text_reponse,
                    "attendue": ", ".join(bonnes),
                })
        # Résultat final
        total_max = quiz.total_points()
        pourcentage = round((score_obtenu / total_max * 100), 1) if total_max > 0 else 0
        print("\n" + "=" * 55)
        print(f"🏁 FIN DU QUIZ ! Score de {user.pseudo} : {score_obtenu} / {total_max} points ({pourcentage}%)")
        print("=" * 55)
        if reponses_incorrectes:
            print("\n📖 Récapitulatif des erreurs :")
            for err in reponses_incorrectes:
                print(f" • Question : {err['question']}")
                print(f"   Votre réponse : {err['choisie']} ❌")
    
    def menu_administrateur(self, user: User) -> None:
        """Menu interactif pour un utilisateur ayant le rôle 'admin'."""
        while self.auth_service.is_authenticated():
            print("\n" + "=" * 50)
            print(f"  ESPACE ADMINISTRATEUR - Connecté : {user.pseudo}")
            print("=" * 50)
            print("1.  Voir mon profil")
            print("2.  Lister les utilisateurs enregistrés")
            print("3.  Créer un quiz manuellement (Sprint 3 - Tâche 3.1)")
            print("4.  Importer un quiz depuis un fichier texte (Sprint 3 - Tâche 3.2)")
            print("5.  Se déconnecter")
            print("-" * 50)

            choix = input("Votre choix (1-5) : ").strip()

            if choix == "1":
                self.afficher_profil(user)
            elif choix == "2":
                self.lister_utilisateurs()
            elif choix == "3":
                self.action_creer_quiz(user)
            elif choix == "4":
                self.action_importer_quiz(user)
            elif choix == "5":
                self.auth_service.logout()
                print("\n Déconnexion réussie.")
                break
            else:
                print(" Choix invalide.")

    def action_creer_quiz(self, user: User) -> None:
        """Formulaire interactif de création manuelle d'un quiz (Tâche 3.1)."""
        print("\n" + "=" * 50)
        print("CRÉATION D'UN NOUVEAU QUIZ")
        print("=" * 50)
        titre = input("Titre du quiz : ").strip()
        if not titre:
            print("Erreur : Le titre ne peut pas être vide.")
            input("Appuyez sur [Entrée] pour continuer...")
            return

        description = input("Description (optionnelle) : ").strip()

        questions_data = []
        num_q = 1
        print("\n--- Ajout des questions (tapez 'fin' comme énoncé pour terminer) ---")
        while True:
            print(f"\nQuestion n°{num_q} :")
            enonce = input("Énoncé de la question (ou 'fin' pour terminer) : ").strip()
            if enonce.lower() == "fin":
                break
            if not enonce:
                print("Erreur : L'énoncé ne peut pas être vide.")
                continue

            pts_input = input("Nombre de points pour cette question [défaut 1] : ").strip()
            points = int(pts_input) if pts_input.isdigit() and int(pts_input) > 0 else 1

            reponses = []
            print("Saisissez les propositions de réponses (min. 2) :")
            for i in range(1, 5):
                rep_texte = input(f"  Option {i} (ou laissez vide pour arrêter) : ").strip()
                if not rep_texte:
                    if len(reponses) < 2:
                        print("  Attention : Il faut au moins 2 propositions de réponse.")
                        continue
                    break
                reponses.append({"texte": rep_texte, "est_correct": False})

            print("Quelle est la bonne réponse ?")
            for idx, r in enumerate(reponses, 1):
                print(f"  {idx}. {r['texte']}")

            while True:
                choix_bonne = input(f"Numéro de la bonne réponse (1-{len(reponses)}) : ").strip()
                if choix_bonne.isdigit() and 1 <= int(choix_bonne) <= len(reponses):
                    reponses[int(choix_bonne) - 1]["est_correct"] = True
                    break
                print("Choix invalide.")

            questions_data.append({"enonce": enonce, "points": points, "reponses": reponses})
            num_q += 1

        if not questions_data:
            print("\nAucun quiz créé (aucune question ajoutée).")
            input("Appuyez sur [Entrée] pour continuer...")
            return

        succes, message, quiz = self.quiz_service.creer_quiz_manuel(
            titre=titre,
            description=description,
            auteur=user,
            questions_data=questions_data,
        )

        if succes:
            print(f"\n[OK] {message}")
        else:
            print(f"\n[Erreur] {message}")
        input("Appuyez sur [Entrée] pour continuer...")

    def action_importer_quiz(self, user: User) -> None:
        """Importation d'un quiz depuis un fichier texte (Tâche 3.2)."""
        print("\n" + "=" * 50)
        print("IMPORTATION D'UN QUIZ DEPUIS UN FICHIER TEXTE (.TXT)")
        print("=" * 50)
        chemin = input("Chemin du fichier (ex: data/sample_quiz.txt) : ").strip()
        if not chemin:
            print("Erreur : Chemin non renseigné.")
            input("Appuyez sur [Entrée] pour continuer...")
            return

        succes, message, quiz = self.quiz_service.importer_quiz_depuis_fichier(chemin, auteur=user)
        if succes:
            print(f"\n[OK] {message}")
        else:
            print(f"\n[Erreur] {message}")
        input("Appuyez sur [Entrée] pour continuer...")

    def afficher_profil(self, user: User) -> None:
        """Affiche les informations personnelles de l'utilisateur."""
        print("\n---  PROFIL UTILISATEUR ---")
        print(f"Identifiant unique : {user.id_utilisateur}")
        print(f"Pseudo             : {user.pseudo}")
        print(f"E-mail             : {user.email}")
        print(f"Rôle               : {user.role.upper()}")
        print(f"Date d'inscription : {user.date_creation}")
        input("\nAppuyez sur [Entrée] pour continuer...")

    def lister_utilisateurs(self) -> None:
        """Affiche la liste de tous les utilisateurs enregistrés."""
        users = self.auth_service.list_users()
        print("\n---  LISTE DES UTILISATEURS DU SYSTÈME ---")
        print(f"{'Pseudo':<20} {'Rôle':<10} {'Email':<30}")
        print("-" * 62)
        for u in users:
            print(f"{u.pseudo:<20} {u.role:<10} {u.email:<30}")
        print("-" * 62)
        print(f"Total : {len(users)} utilisateur(s) enregistré(s).")
        input("\nAppuyez sur [Entrée] pour continuer...")


def lancer() -> None:
    """Démarre l'interface en ligne de commande."""
    try:
        app = QuizAppCLI()
        app.menu_principal()
    except KeyboardInterrupt:
        print("\n\nFermeture de l'application...")
        sys.exit(0)
