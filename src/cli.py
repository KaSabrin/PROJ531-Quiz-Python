"""Interface utilisateur en ligne de commande (CLI) de l'application Quizora.

Ce module contient les menus. Le point d'entrée du programme est le fichier
main.py situé à la racine du dépôt.
"""

import getpass
import sys
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.storage_service import StorageService


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

    def afficher_banniere(self) -> None:
        """Affiche le titre stylisé de l'application."""
        print("\n" + "=" * 60)
        print("              🎓 QUIZORA - PROJ531 QUIZ PYTHON 🎓          ")
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
                print("\nMerci d'avoir utilisé Quiz Python. À bientôt !\n")
                sys.exit(0)
            else:
                print("\n Option invalide. Veuillez entrer un nombre entre 1 et 4.")

    def action_a_propos(self) -> None:
        """Affiche les informations du projet et les comptes de démo."""
        print("\n" + "-" * 50)
        print("ℹ  INFORMATIONS DU PROJET & COMPTES DE TEST")
        print("-" * 50)
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
                print("\n[Sprint 3] Le module de passation de quiz sera intégré lors du Sprint 3.")
                input("Appuyez sur [Entrée] pour continuer...")
            elif choix == "3":
                print("\n[Sprint 4] L'historique détaillé des scores sera intégré lors du Sprint 4.")
                input("Appuyez sur [Entrée] pour continuer...")
            elif choix == "4":
                self.auth_service.logout()
                print("\n👋 Vous avez été déconnecté avec succès.")
                break
            else:
                print(" Choix invalide.")

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
                print("\n[Sprint 3 - Tâche 3.1] La création interactive de quiz sera développée lors du prochain sprint.")
                input("Appuyez sur [Entrée] pour continuer...")
            elif choix == "4":
                print("\n[Sprint 3 - Tâche 3.2] L'importateur de quiz depuis fichier texte (.txt) sera développé au prochain sprint.")
                input("Appuyez sur [Entrée] pour continuer...")
            elif choix == "5":
                self.auth_service.logout()
                print("\n Déconnexion réussie.")
                break
            else:
                print(" Choix invalide.")

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
