"""Interface graphique (GUI) moderne pour l'application Quizora avec Tkinter.

Fournit une page de connexion graphique, une page d'inscription et un tableau
de bord adapte au role de l'utilisateur (Joueur / Administrateur).
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from src.models.quiz import Quiz
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.quiz_service import QuizService
from src.services.resultat_service import ResultatService
from src.services.storage_service import StorageService


class QuizoraGUI:
    """Fenetre principale et gestionnaire de pages graphiques pour Quizora."""

    # Palette de couleurs moderne (Slate & Blue)
    COLOR_BG = "#0f172a"          # Slate 900
    COLOR_CARD = "#1e293b"        # Slate 800
    COLOR_BORDER = "#334155"      # Slate 700
    COLOR_TEXT = "#f8fafc"        # Slate 50
    COLOR_MUTED = "#94a3b8"       # Slate 400
    COLOR_PRIMARY = "#2563eb"     # Blue 600
    COLOR_PRIMARY_HOVER = "#1d4ed8"
    COLOR_SUCCESS = "#10b981"     # Emerald 500
    COLOR_ERROR = "#ef4444"       # Red 500
    COLOR_INPUT_BG = "#0f172a"
    COLOR_INPUT_FG = "#ffffff"

    def __init__(self, root: Optional[tk.Tk] = None):
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        self.storage_service = StorageService()
        self.auth_service = AuthService(storage_service=self.storage_service)
        self.quiz_service = QuizService(storage_service=self.storage_service)
        self.resultat_service = ResultatService(storage_service=self.storage_service)

        self.current_user: Optional[User] = None

        # Configuration de la fenetre
        self.root.title("Quizora - PROJ531 USMB (Interface Graphique)")
        self.root.geometry("820x680")
        self.root.minsize(760, 600)
        self.root.configure(bg=self.COLOR_BG)

        # Centrage a l'ecran
        self._centrer_fenetre(820, 680)

        # Configuration du style ttk
        self._configurer_styles()

        # Conteneur principal
        self.main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        self.main_container.pack(fill="both", expand=True)

        # Construction du header global
        self._construire_header()

        # Zone dynamique pour les pages (Login / Register / Dashboard)
        self.content_frame = tk.Frame(self.main_container, bg=self.COLOR_BG)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Affichage initial : Page de connexion
        self.afficher_page_connexion()

    def _centrer_fenetre(self, largeur: int, hauteur: int) -> None:
        """Centre la fenetre sur l'ecran de l'utilisateur."""
        self.root.update_idletasks()
        ecran_largeur = self.root.winfo_screenwidth()
        ecran_hauteur = self.root.winfo_screenheight()
        x = max(0, int((ecran_largeur - largeur) / 2))
        y = max(0, int((ecran_hauteur - hauteur) / 2))
        self.root.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    def _configurer_styles(self) -> None:
        """Configure les styles visuels des widgets ttk."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.COLOR_PRIMARY,
            foreground="#ffffff",
            borderwidth=0,
            padding=8,
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.COLOR_PRIMARY_HOVER)],
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 9),
            background=self.COLOR_BORDER,
            foreground="#ffffff",
            borderwidth=0,
            padding=6,
        )

    def _construire_header(self) -> None:
        """Affiche le bandeau superieur commun a toutes les pages."""
        header_frame = tk.Frame(self.main_container, bg=self.COLOR_CARD, height=70)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Titre application
        titre_label = tk.Label(
            header_frame,
            text="QUIZORA",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        )
        titre_label.pack(side="left", padx=25, pady=12)

        # Sous-titre académique
        sub_label = tk.Label(
            header_frame,
            text="Gestion et Passation de Quiz | PROJ531 - USMB",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        )
        sub_label.pack(side="left", pady=16)

        # Zone droite du header (statut utilisateur)
        self.header_user_frame = tk.Frame(header_frame, bg=self.COLOR_CARD)
        self.header_user_frame.pack(side="right", padx=25, pady=12)

    def _nettoyer_contenu(self) -> None:
        """Vide la zone centrale pour afficher une nouvelle page."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # =========================================================================
    # PAGE 1 : CONNEXION (LOGIN)
    # =========================================================================

    def afficher_page_connexion(self) -> None:
        """Construit et affiche la page graphique de connexion."""
        self._nettoyer_contenu()
        self._mettre_a_jour_header_deconnecte()

        # Carte centrale
        card = tk.Frame(
            self.content_frame,
            bg=self.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=520)

        # Titre de la page
        lbl_titre = tk.Label(
            card,
            text="Connexion à votre compte",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        )
        lbl_titre.pack(pady=(25, 4))

        lbl_desc = tk.Label(
            card,
            text="Entrez vos identifiants pour accéder à l'espace Quizora",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        )
        lbl_desc.pack(pady=(0, 20))

        # Formulaire
        form_frame = tk.Frame(card, bg=self.COLOR_CARD)
        form_frame.pack(fill="x", padx=45)

        # Champ Identifiant
        lbl_id = tk.Label(
            form_frame,
            text="Identifiant (Pseudo ou E-mail) :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        )
        lbl_id.pack(fill="x", pady=(0, 4))

        entree_id = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_id.pack(fill="x", ipady=6, pady=(0, 14))

        # Champ Mot de passe
        lbl_pwd = tk.Label(
            form_frame,
            text="Mot de passe :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        )
        lbl_pwd.pack(fill="x", pady=(0, 4))

        pwd_frame = tk.Frame(form_frame, bg=self.COLOR_INPUT_BG)
        pwd_frame.pack(fill="x", pady=(0, 10))

        entree_pwd = tk.Entry(
            pwd_frame,
            show="*",
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_pwd.pack(side="left", fill="x", expand=True, ipady=6)

        # Bouton Afficher / Masquer
        def toggle_password():
            if entree_pwd.cget("show") == "":
                entree_pwd.config(show="*")
                btn_toggle.config(text="Afficher")
            else:
                entree_pwd.config(show="")
                btn_toggle.config(text="Masquer")

        btn_toggle = tk.Button(
            pwd_frame,
            text="Afficher",
            font=("Segoe UI", 8),
            bg=self.COLOR_BORDER,
            fg=self.COLOR_TEXT,
            relief="flat",
            padx=8,
            command=toggle_password,
        )
        btn_toggle.pack(side="right", padx=(4, 0), ipady=5)

        # Message d'erreur ou d'information
        lbl_feedback = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            wraplength=420,
        )
        lbl_feedback.pack(pady=4)

        # Action de connexion
        def tenter_connexion():
            identifiant = entree_id.get().strip()
            mot_de_passe = entree_pwd.get()

            if not identifiant or not mot_de_passe:
                lbl_feedback.config(
                    text="Erreur : Veuillez renseigner l'identifiant et le mot de passe.",
                    fg=self.COLOR_ERROR,
                )
                return

            succes, message, user = self.auth_service.login(identifiant, mot_de_passe)
            if succes and user is not None:
                self.current_user = user
                lbl_feedback.config(text="[OK] Connexion réussie !", fg=self.COLOR_SUCCESS)
                self.root.after(350, self.afficher_page_dashboard)
            else:
                lbl_feedback.config(text=f"Erreur : {message}", fg=self.COLOR_ERROR)

        # Validation avec la touche Entrée
        entree_id.bind("<Return>", lambda e: entree_pwd.focus_set())
        entree_pwd.bind("<Return>", lambda e: tenter_connexion())

        # Bouton principal Se Connecter
        btn_connexion = tk.Button(
            card,
            text="Se connecter",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_PRIMARY,
            fg="#ffffff",
            activebackground=self.COLOR_PRIMARY_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=tenter_connexion,
        )
        btn_connexion.pack(fill="x", padx=45, ipady=8, pady=(8, 12))

        # Comptes de test rapide (Admin / Joueur)
        demo_frame = tk.Frame(card, bg=self.COLOR_CARD)
        demo_frame.pack(fill="x", padx=45, pady=(0, 10))

        def pre_remplir(pseudo: str, mdp: str):
            entree_id.delete(0, tk.END)
            entree_id.insert(0, pseudo)
            entree_pwd.delete(0, tk.END)
            entree_pwd.insert(0, mdp)
            lbl_feedback.config(text="")

        btn_demo_admin = tk.Button(
            demo_frame,
            text="Compte Admin",
            font=("Segoe UI", 8),
            bg=self.COLOR_BORDER,
            fg=self.COLOR_TEXT,
            relief="flat",
            cursor="hand2",
            command=lambda: pre_remplir("admin", "Admin123!"),
        )
        btn_demo_admin.pack(side="left", fill="x", expand=True, padx=(0, 4), ipady=4)

        btn_demo_joueur = tk.Button(
            demo_frame,
            text="Compte Joueur",
            font=("Segoe UI", 8),
            bg=self.COLOR_BORDER,
            fg=self.COLOR_TEXT,
            relief="flat",
            cursor="hand2",
            command=lambda: pre_remplir("joueur1", "Joueur123!"),
        )
        btn_demo_joueur.pack(side="right", fill="x", expand=True, padx=(4, 0), ipady=4)

        # Lien vers inscription
        sep = tk.Frame(card, bg=self.COLOR_BORDER, height=1)
        sep.pack(fill="x", padx=45, pady=(8, 10))

        lbl_switch = tk.Label(
            card,
            text="Pas encore de compte ?",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        )
        lbl_switch.pack()

        btn_aller_inscription = tk.Button(
            card,
            text="Créer un nouveau compte",
            font=("Segoe UI", 9, "underline"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_PRIMARY,
            bd=0,
            cursor="hand2",
            activebackground=self.COLOR_CARD,
            activeforeground=self.COLOR_PRIMARY_HOVER,
            command=self.afficher_page_inscription,
        )
        btn_aller_inscription.pack(pady=(2, 10))

        # Focus automatique
        entree_id.focus_set()

    # =========================================================================
    # PAGE 2 : INSCRIPTION (REGISTER)
    # =========================================================================

    def afficher_page_inscription(self) -> None:
        """Construit et affiche la page graphique de creation de compte."""
        self._nettoyer_contenu()
        self._mettre_a_jour_header_deconnecte()

        card = tk.Frame(
            self.content_frame,
            bg=self.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=540, height=560)

        # Titre
        lbl_titre = tk.Label(
            card,
            text="Inscription à Quizora",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        )
        lbl_titre.pack(pady=(20, 2))

        lbl_desc = tk.Label(
            card,
            text="Créez votre compte pour participer aux quiz",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        )
        lbl_desc.pack(pady=(0, 15))

        form_frame = tk.Frame(card, bg=self.COLOR_CARD)
        form_frame.pack(fill="x", padx=45)

        # Pseudo
        tk.Label(
            form_frame,
            text="Pseudo (3 à 30 caractères) :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        entree_pseudo = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_pseudo.pack(fill="x", ipady=5, pady=(2, 8))

        # E-mail
        tk.Label(
            form_frame,
            text="Adresse e-mail :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        entree_email = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_email.pack(fill="x", ipady=5, pady=(2, 8))

        # Mot de passe
        tk.Label(
            form_frame,
            text="Mot de passe (min. 6 car., lettres + chiffres) :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        entree_pwd = tk.Entry(
            form_frame,
            show="*",
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_pwd.pack(fill="x", ipady=5, pady=(2, 8))

        # Confirmation mot de passe
        tk.Label(
            form_frame,
            text="Confirmer le mot de passe :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        entree_pwd_conf = tk.Entry(
            form_frame,
            show="*",
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree_pwd_conf.pack(fill="x", ipady=5, pady=(2, 10))

        # Feedback
        lbl_feedback = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            wraplength=440,
        )
        lbl_feedback.pack(pady=2)

        def tenter_inscription():
            pseudo = entree_pseudo.get().strip()
            email = entree_email.get().strip()
            pwd = entree_pwd.get()
            pwd_conf = entree_pwd_conf.get()

            if pwd != pwd_conf:
                lbl_feedback.config(
                    text="Erreur : Les deux mots de passe ne correspondent pas.",
                    fg=self.COLOR_ERROR,
                )
                return

            succes, message, new_user = self.auth_service.register(
                pseudo=pseudo,
                email=email,
                password=pwd,
                role=User.ROLE_JOUEUR,
            )

            if succes:
                lbl_feedback.config(
                    text="[OK] Inscription validée ! Redirection vers la connexion...",
                    fg=self.COLOR_SUCCESS,
                )
                self.root.after(1200, self.afficher_page_connexion)
            else:
                lbl_feedback.config(text=f"Erreur : {message}", fg=self.COLOR_ERROR)

        btn_inscrire = tk.Button(
            card,
            text="Valider mon inscription",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_PRIMARY,
            fg="#ffffff",
            activebackground=self.COLOR_PRIMARY_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=tenter_inscription,
        )
        btn_inscrire.pack(fill="x", padx=45, ipady=8, pady=(8, 10))

        btn_retour = tk.Button(
            card,
            text="< Retour à la connexion",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
            bd=0,
            cursor="hand2",
            command=self.afficher_page_connexion,
        )
        btn_retour.pack(pady=(0, 10))

        entree_pseudo.focus_set()

    # =========================================================================
    # PAGE 3 : TABLEAU DE BORD (DASHBOARD APRÈS CONNEXION)
    # =========================================================================

    def afficher_page_dashboard(self) -> None:
        """Affiche le tableau de bord connecte de l'utilisateur."""
        if not self.current_user:
            self.afficher_page_connexion()
            return

        self._nettoyer_contenu()
        self._mettre_a_jour_header_connecte()

        # En-tete du dashboard
        top_frame = tk.Frame(self.content_frame, bg=self.COLOR_BG)
        top_frame.pack(fill="x", pady=(0, 20))

        role_label = "ADMINISTRATEUR" if self.current_user.is_admin() else "JOUEUR"
        role_color = self.COLOR_PRIMARY if self.current_user.is_admin() else self.COLOR_SUCCESS

        lbl_bienvenue = tk.Label(
            top_frame,
            text=f"Bienvenue, {self.current_user.pseudo} !",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT,
        )
        lbl_bienvenue.pack(side="left")

        badge_role = tk.Label(
            top_frame,
            text=f"[{role_label}]",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_CARD,
            fg=role_color,
            padx=10,
            pady=4,
        )
        badge_role.pack(side="right")

        # Disposition en grille : Carte Profil (gauche) et Actions / Quiz (droite)
        corps = tk.Frame(self.content_frame, bg=self.COLOR_BG)
        corps.pack(fill="both", expand=True)

        # 1. Carte Profil utilisateur
        carte_profil = tk.Frame(
            corps,
            bg=self.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
            width=280,
        )
        carte_profil.pack(side="left", fill="y", padx=(0, 15), ipady=10)
        carte_profil.pack_propagate(False)

        tk.Label(
            carte_profil,
            text="PROFIL UTILISATEUR",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        ).pack(anchor="w", padx=20, pady=(15, 10))

        def add_info_row(titre: str, valeur: str):
            f = tk.Frame(carte_profil, bg=self.COLOR_CARD)
            f.pack(fill="x", padx=20, pady=4)
            tk.Label(
                f, text=titre, font=("Segoe UI", 8), bg=self.COLOR_CARD, fg=self.COLOR_MUTED
            ).pack(anchor="w")
            tk.Label(
                f, text=valeur, font=("Segoe UI", 9, "bold"), bg=self.COLOR_CARD, fg=self.COLOR_TEXT
            ).pack(anchor="w")

        add_info_row("Pseudo", self.current_user.pseudo)
        add_info_row("Adresse e-mail", self.current_user.email)
        add_info_row("Rôle", self.current_user.role.capitalize())
        add_info_row("Identifiant unique", self.current_user.id_utilisateur[:13] + "...")
        add_info_row("Date de création", self.current_user.date_creation[:19])

        btn_deconnexion = tk.Button(
            carte_profil,
            text="Se déconnecter",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BORDER,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.deconnecter,
        )
        btn_deconnexion.pack(side="bottom", fill="x", padx=20, pady=15, ipady=6)

        # 2. Carte Principale (Catalogue & Actions)
        carte_principale = tk.Frame(
            corps,
            bg=self.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        carte_principale.pack(side="right", fill="both", expand=True)

        titre_section = (
            "ESPACE ADMINISTRATION - GESTION DES QUIZ"
            if self.current_user.is_admin()
            else "ESPACE JOUEUR - CATALOGUE DES QUIZ"
        )
        tk.Label(
            carte_principale,
            text=titre_section,
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # Chargement et affichage des quiz disponibles
        quizzes = self.quiz_service.lister_quiz()

        stats_frame = tk.Frame(carte_principale, bg=self.COLOR_CARD)
        stats_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(
            stats_frame,
            text=f"Total de quiz disponibles : {len(quizzes)}",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        ).pack(side="left")

        # Barre d'actions selon le role
        actions_frame = tk.Frame(carte_principale, bg=self.COLOR_CARD)
        actions_frame.pack(fill="x", padx=20, pady=(0, 10))

        if self.current_user.is_admin():
            self._bouton(
                actions_frame, "+ Créer un quiz", self.afficher_page_creation_quiz
            ).pack(side="left", padx=(0, 6), ipady=4)
            self._bouton(
                actions_frame, "Importer un fichier (.txt)", self.importer_quiz_fichier,
                secondaire=True,
            ).pack(side="left", ipady=4)
        else:
            self._bouton(
                actions_frame, "Mon historique de scores", self.afficher_page_historique,
                secondaire=True,
            ).pack(side="left", ipady=4)

        # Liste deroulante des quiz
        list_container = tk.Frame(carte_principale, bg=self.COLOR_CARD)
        list_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        scrollable_frame = self._zone_defilante(list_container)

        if not quizzes:
            tk.Label(
                scrollable_frame,
                text="Aucun quiz disponible pour le moment.",
                font=("Segoe UI", 9, "italic"),
                bg=self.COLOR_CARD,
                fg=self.COLOR_MUTED,
            ).pack(pady=30)
        else:
            for idx, q in enumerate(quizzes, 1):
                item = tk.Frame(
                    scrollable_frame,
                    bg=self.COLOR_BORDER,
                    bd=0,
                    padx=12,
                    pady=8,
                )
                item.pack(fill="x", expand=True, pady=4)

                if not self.current_user.is_admin():
                    self._bouton(
                        item, "Jouer", lambda quiz=q: self.afficher_page_passage(quiz)
                    ).pack(side="right", padx=(8, 0))

                tk.Label(
                    item,
                    text=f"{idx}. {q.titre}",
                    font=("Segoe UI", 10, "bold"),
                    bg=self.COLOR_BORDER,
                    fg=self.COLOR_TEXT,
                    anchor="w",
                ).pack(fill="x")

                desc = q.description if q.description else "Aucune description"
                tk.Label(
                    item,
                    text=f"{len(q.questions)} question(s) | {q.total_points()} points | {desc}",
                    font=("Segoe UI", 8),
                    bg=self.COLOR_BORDER,
                    fg=self.COLOR_MUTED,
                    anchor="w",
                ).pack(fill="x")

    # =========================================================================
    # OUTILS COMMUNS (boutons, champs, zones defilantes)
    # =========================================================================

    def _bouton(self, parent, texte: str, commande, secondaire: bool = False) -> tk.Button:
        """Cree un bouton plat au style de l'application."""
        bg = self.COLOR_BORDER if secondaire else self.COLOR_PRIMARY
        return tk.Button(
            parent,
            text=texte,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg="#ffffff",
            activebackground=self.COLOR_PRIMARY_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=commande,
        )

    def _champ(self, parent, libelle: str) -> tk.Entry:
        """Cree un libelle suivi d'un champ de saisie, et retourne le champ."""
        tk.Label(
            parent,
            text=libelle,
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        entree = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
        )
        entree.pack(fill="x", ipady=4, pady=(2, 8))
        return entree

    def _carte(self, parent) -> tk.Frame:
        """Cree un cadre de type carte."""
        return tk.Frame(
            parent,
            bg=self.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )

    def _zone_defilante(self, parent) -> tk.Frame:
        """Cree une zone avec barre de defilement et retourne le cadre interieur."""
        canvas = tk.Canvas(parent, bg=self.COLOR_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        interieur = tk.Frame(canvas, bg=self.COLOR_CARD)

        interieur.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        fenetre = canvas.create_window((0, 0), window=interieur, anchor="nw")
        # Le cadre interieur suit la largeur du canvas
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(fenetre, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return interieur

    def _entete_page(self, titre: str) -> None:
        """Affiche le titre d'une page et un bouton de retour au tableau de bord."""
        top = tk.Frame(self.content_frame, bg=self.COLOR_BG)
        top.pack(fill="x", pady=(0, 12))
        tk.Label(
            top,
            text=titre,
            font=("Segoe UI", 16, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT,
        ).pack(side="left")
        self._bouton(
            top, "< Retour", self.afficher_page_dashboard, secondaire=True
        ).pack(side="right", ipady=3)

    # =========================================================================
    # ADMIN : CREATION ET IMPORT DE QUIZ
    # =========================================================================

    def afficher_page_creation_quiz(self) -> None:
        """Formulaire graphique de creation manuelle d'un quiz (admin)."""
        self._nettoyer_contenu()
        self._entete_page("Créer un nouveau quiz")

        questions_data: list[dict] = []

        corps = tk.Frame(self.content_frame, bg=self.COLOR_BG)
        corps.pack(fill="both", expand=True)

        # --- Colonne gauche : informations du quiz et questions ajoutees ---
        gauche = self._carte(corps)
        gauche.pack(side="left", fill="both", expand=True, padx=(0, 10))
        g = tk.Frame(gauche, bg=self.COLOR_CARD)
        g.pack(fill="both", expand=True, padx=16, pady=12)

        entree_titre = self._champ(g, "Titre du quiz :")
        entree_desc = self._champ(g, "Description (optionnelle) :")

        tk.Label(
            g,
            text="Questions ajoutées :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")
        liste_questions = tk.Listbox(
            g,
            font=("Segoe UI", 9),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_TEXT,
            selectbackground=self.COLOR_PRIMARY,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
            height=8,
        )
        liste_questions.pack(fill="both", expand=True, pady=(2, 6))

        def retirer_question():
            selection = liste_questions.curselection()
            if not selection:
                return
            idx = selection[0]
            del questions_data[idx]
            rafraichir_liste()

        def rafraichir_liste():
            liste_questions.delete(0, tk.END)
            for i, q in enumerate(questions_data, 1):
                liste_questions.insert(tk.END, f"{i}. {q['enonce']} ({q['points']} pt)")

        self._bouton(
            g, "Retirer la question sélectionnée", retirer_question, secondaire=True
        ).pack(fill="x", ipady=2)

        lbl_feedback = tk.Label(
            g,
            text="",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            wraplength=300,
            justify="left",
        )
        lbl_feedback.pack(fill="x", pady=6)

        def enregistrer_quiz():
            succes, message, _ = self.quiz_service.creer_quiz_manuel(
                titre=entree_titre.get(),
                description=entree_desc.get(),
                auteur=self.current_user,
                questions_data=questions_data,
            )
            if succes:
                messagebox.showinfo("Quizora", message)
                self.afficher_page_dashboard()
            else:
                lbl_feedback.config(text=f"Erreur : {message}", fg=self.COLOR_ERROR)

        self._bouton(g, "Enregistrer le quiz", enregistrer_quiz).pack(fill="x", ipady=6)

        # --- Colonne droite : saisie d'une question ---
        droite = self._carte(corps)
        droite.pack(side="right", fill="both", expand=True)
        d = tk.Frame(droite, bg=self.COLOR_CARD)
        d.pack(fill="both", expand=True, padx=16, pady=12)

        lbl_num = tk.Label(
            d,
            text="Nouvelle question",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        )
        lbl_num.pack(fill="x", pady=(0, 6))

        entree_enonce = self._champ(d, "Énoncé :")

        pts_frame = tk.Frame(d, bg=self.COLOR_CARD)
        pts_frame.pack(fill="x", pady=(0, 8))
        tk.Label(
            pts_frame,
            text="Points :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        ).pack(side="left")
        spin_points = tk.Spinbox(
            pts_frame,
            from_=1,
            to=20,
            width=5,
            font=("Segoe UI", 10),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_INPUT_FG,
            buttonbackground=self.COLOR_BORDER,
            relief="flat",
        )
        spin_points.pack(side="left", padx=8)

        tk.Label(
            d,
            text="Propositions (cochez la bonne réponse, min. 2) :",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x")

        bonne_reponse = tk.IntVar(value=0)
        entrees_options: list[tk.Entry] = []
        for i in range(4):
            ligne = tk.Frame(d, bg=self.COLOR_CARD)
            ligne.pack(fill="x", pady=3)
            tk.Radiobutton(
                ligne,
                variable=bonne_reponse,
                value=i,
                bg=self.COLOR_CARD,
                activebackground=self.COLOR_CARD,
                selectcolor=self.COLOR_INPUT_BG,
            ).pack(side="left")
            e = tk.Entry(
                ligne,
                font=("Segoe UI", 10),
                bg=self.COLOR_INPUT_BG,
                fg=self.COLOR_INPUT_FG,
                insertbackground="white",
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.COLOR_BORDER,
            )
            e.pack(side="left", fill="x", expand=True, ipady=3)
            entrees_options.append(e)

        lbl_q_feedback = tk.Label(
            d,
            text="",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_ERROR,
            wraplength=300,
            justify="left",
        )
        lbl_q_feedback.pack(fill="x", pady=6)

        def ajouter_question():
            enonce = entree_enonce.get().strip()
            if not enonce:
                lbl_q_feedback.config(text="Erreur : L'énoncé est vide.", fg=self.COLOR_ERROR)
                return
            try:
                points = int(spin_points.get())
            except ValueError:
                points = 0
            if points < 1:
                lbl_q_feedback.config(text="Erreur : Points invalides.", fg=self.COLOR_ERROR)
                return

            reponses = []
            bonne_choisie = False
            for i, e in enumerate(entrees_options):
                texte = e.get().strip()
                if not texte:
                    continue
                est_correct = i == bonne_reponse.get()
                bonne_choisie = bonne_choisie or est_correct
                reponses.append({"texte": texte, "est_correct": est_correct})

            if len(reponses) < 2:
                lbl_q_feedback.config(
                    text="Erreur : Il faut au moins 2 propositions.", fg=self.COLOR_ERROR
                )
                return
            if not bonne_choisie:
                lbl_q_feedback.config(
                    text="Erreur : La bonne réponse cochée est vide.", fg=self.COLOR_ERROR
                )
                return

            questions_data.append({"enonce": enonce, "points": points, "reponses": reponses})
            rafraichir_liste()

            # Remise a zero du formulaire de question
            entree_enonce.delete(0, tk.END)
            for e in entrees_options:
                e.delete(0, tk.END)
            spin_points.delete(0, tk.END)
            spin_points.insert(0, "1")
            bonne_reponse.set(0)
            lbl_q_feedback.config(
                text=f"[OK] Question {len(questions_data)} ajoutée.", fg=self.COLOR_SUCCESS
            )
            entree_enonce.focus_set()

        self._bouton(d, "Ajouter cette question", ajouter_question).pack(fill="x", ipady=6)

        entree_titre.focus_set()

    def importer_quiz_fichier(self) -> None:
        """Ouvre un selecteur de fichier puis importe le quiz (admin)."""
        chemin = filedialog.askopenfilename(
            title="Importer un quiz",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        )
        if not chemin:
            return
        succes, message, _ = self.quiz_service.importer_quiz_depuis_fichier(
            chemin, auteur=self.current_user
        )
        if succes:
            messagebox.showinfo("Quizora", message)
            self.afficher_page_dashboard()
        else:
            messagebox.showerror("Quizora", message)

    # =========================================================================
    # JOUEUR : PASSAGE D'UN QUIZ, RESULTAT ET HISTORIQUE
    # =========================================================================

    def afficher_page_passage(self, quiz: Quiz) -> None:
        """Lance le passage interactif d'un quiz, question par question."""
        if not quiz.questions:
            messagebox.showwarning(
                "Quizora", f"Le quiz « {quiz.titre} » ne contient aucune question."
            )
            return

        etat = {"index": 0, "score": 0, "erreurs": [], "valide": False}

        self._nettoyer_contenu()
        self._entete_page(quiz.titre)

        card = self._carte(self.content_frame)
        card.pack(fill="both", expand=True)
        zone = tk.Frame(card, bg=self.COLOR_CARD)
        zone.pack(fill="both", expand=True, padx=30, pady=20)

        lbl_progression = tk.Label(
            zone, font=("Segoe UI", 9), bg=self.COLOR_CARD, fg=self.COLOR_MUTED, anchor="w"
        )
        lbl_progression.pack(fill="x")
        lbl_enonce = tk.Label(
            zone,
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            anchor="w",
            justify="left",
            wraplength=680,
        )
        lbl_enonce.pack(fill="x", pady=(6, 14))

        options_frame = tk.Frame(zone, bg=self.COLOR_CARD)
        options_frame.pack(fill="x")
        choix = tk.IntVar(value=-1)

        lbl_feedback = tk.Label(
            zone,
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_CARD,
            anchor="w",
            justify="left",
            wraplength=680,
        )
        lbl_feedback.pack(fill="x", pady=12)

        btn_action = self._bouton(zone, "Valider", lambda: action())
        btn_action.pack(anchor="e", ipady=6, ipadx=10)

        def afficher_question():
            question = quiz.questions[etat["index"]]
            etat["valide"] = False
            choix.set(-1)
            lbl_progression.config(
                text=f"Question {etat['index'] + 1}/{len(quiz.questions)}"
                f"  |  {question.points} pt(s)"
            )
            lbl_enonce.config(text=question.enonce)
            lbl_feedback.config(text="")
            btn_action.config(text="Valider")
            for w in options_frame.winfo_children():
                w.destroy()
            for i, rep in enumerate(question.reponses):
                tk.Radiobutton(
                    options_frame,
                    text=rep.text_reponse,
                    variable=choix,
                    value=i,
                    font=("Segoe UI", 10),
                    bg=self.COLOR_CARD,
                    fg=self.COLOR_TEXT,
                    activebackground=self.COLOR_CARD,
                    activeforeground=self.COLOR_TEXT,
                    selectcolor=self.COLOR_INPUT_BG,
                    anchor="w",
                    justify="left",
                    wraplength=640,
                ).pack(fill="x", pady=3)

        def action():
            if etat["valide"]:
                etat["index"] += 1
                if etat["index"] < len(quiz.questions):
                    afficher_question()
                else:
                    self._afficher_page_resultat(quiz, etat["score"], etat["erreurs"])
                return

            idx = choix.get()
            question = quiz.questions[etat["index"]]
            if idx < 0:
                lbl_feedback.config(text="Choisissez une réponse.", fg=self.COLOR_ERROR)
                return

            etat["valide"] = True
            for w in options_frame.winfo_children():
                w.config(state="disabled")
            if question.reponses[idx].est_correct:
                etat["score"] += question.points
                lbl_feedback.config(text="[OK] Bonne réponse !", fg=self.COLOR_SUCCESS)
            else:
                attendue = ", ".join(r.text_reponse for r in question.get_bonnes_reponses())
                etat["erreurs"].append({
                    "question": question.enonce,
                    "choisie": question.reponses[idx].text_reponse,
                    "attendue": attendue,
                })
                lbl_feedback.config(
                    text=f"Mauvaise réponse. Réponse attendue : {attendue}",
                    fg=self.COLOR_ERROR,
                )
            dernier = etat["index"] == len(quiz.questions) - 1
            btn_action.config(text="Voir le résultat" if dernier else "Question suivante")

        afficher_question()

    def _afficher_page_resultat(self, quiz: Quiz, score: int, erreurs: list[dict]) -> None:
        """Enregistre le score et affiche le bilan du quiz."""
        succes, message, _ = self.resultat_service.enregistrer_resultat(
            self.current_user, quiz, score
        )
        total = quiz.total_points()
        pourcentage = round(score / total * 100, 1) if total > 0 else 0

        self._nettoyer_contenu()
        self._entete_page("Résultat du quiz")

        card = self._carte(self.content_frame)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text=quiz.titre,
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        ).pack(pady=(20, 4))
        tk.Label(
            card,
            text=f"{score} / {total} points  ({pourcentage}%)",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_SUCCESS if pourcentage >= 50 else self.COLOR_ERROR,
        ).pack(pady=4)
        tk.Label(
            card,
            text=message,
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED if succes else self.COLOR_ERROR,
        ).pack(pady=(0, 12))

        recap = tk.Frame(card, bg=self.COLOR_CARD)
        recap.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        interieur = self._zone_defilante(recap)

        if not erreurs:
            tk.Label(
                interieur,
                text="Félicitations ! Un sans-faute !",
                font=("Segoe UI", 11, "bold"),
                bg=self.COLOR_CARD,
                fg=self.COLOR_SUCCESS,
            ).pack(pady=20)
        else:
            tk.Label(
                interieur,
                text="Récapitulatif des erreurs :",
                font=("Segoe UI", 10, "bold"),
                bg=self.COLOR_CARD,
                fg=self.COLOR_TEXT,
                anchor="w",
            ).pack(fill="x", pady=(0, 6))
            for err in erreurs:
                item = tk.Frame(interieur, bg=self.COLOR_BORDER, padx=12, pady=8)
                item.pack(fill="x", pady=4)
                for texte, couleur in (
                    (err["question"], self.COLOR_TEXT),
                    (f"Votre réponse : {err['choisie']}", self.COLOR_ERROR),
                    (f"Réponse attendue : {err['attendue']}", self.COLOR_SUCCESS),
                ):
                    tk.Label(
                        item,
                        text=texte,
                        font=("Segoe UI", 9),
                        bg=self.COLOR_BORDER,
                        fg=couleur,
                        anchor="w",
                        justify="left",
                        wraplength=640,
                    ).pack(fill="x")

        self._bouton(
            card, "Retour au tableau de bord", self.afficher_page_dashboard
        ).pack(pady=(0, 16), ipady=6, ipadx=10)

    def afficher_page_historique(self) -> None:
        """Affiche l'historique des scores du joueur connecte."""
        self._nettoyer_contenu()
        self._entete_page("Mon historique de scores")

        card = self._carte(self.content_frame)
        card.pack(fill="both", expand=True)

        stats = self.resultat_service.statistiques_joueur(self.current_user)
        tk.Label(
            card,
            text=f"Quiz passés : {stats['nb_quiz']}   |   Moyenne : {stats['moyenne']}%"
            f"   |   Meilleur score : {stats['meilleur']}%",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        ).pack(pady=(16, 10))

        style = ttk.Style()
        style.configure(
            "Quizora.Treeview",
            background=self.COLOR_INPUT_BG,
            fieldbackground=self.COLOR_INPUT_BG,
            foreground=self.COLOR_TEXT,
            rowheight=24,
        )
        style.configure(
            "Quizora.Treeview.Heading",
            background=self.COLOR_BORDER,
            foreground=self.COLOR_TEXT,
            font=("Segoe UI", 9, "bold"),
        )

        tableau_frame = tk.Frame(card, bg=self.COLOR_CARD)
        tableau_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        colonnes = ("date", "quiz", "score", "pourcentage")
        tableau = ttk.Treeview(
            tableau_frame, columns=colonnes, show="headings", style="Quizora.Treeview"
        )
        for col, titre, largeur, ancre in (
            ("date", "Date", 140, "w"),
            ("quiz", "Quiz", 300, "w"),
            ("score", "Score", 80, "center"),
            ("pourcentage", "%", 80, "center"),
        ):
            tableau.heading(col, text=titre)
            tableau.column(col, width=largeur, anchor=ancre)

        scrollbar = ttk.Scrollbar(tableau_frame, orient="vertical", command=tableau.yview)
        tableau.configure(yscrollcommand=scrollbar.set)
        tableau.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        titres = {q.id_quiz: q.titre for q in self.quiz_service.lister_quiz()}
        for r in self.resultat_service.historique_joueur(self.current_user):
            tableau.insert(
                "",
                tk.END,
                values=(
                    r.date_passage[:16].replace("T", " "),
                    titres.get(r.id_quiz, "(quiz supprime)"),
                    f"{r.score}/{r.score_max}",
                    f"{r.pourcentage:.1f}%",
                ),
            )

    def _mettre_a_jour_header_deconnecte(self) -> None:
        """Nettoie les informations du bandeau quand aucun utilisateur n'est connecte."""
        for w in self.header_user_frame.winfo_children():
            w.destroy()
        tk.Label(
            self.header_user_frame,
            text="Non connecté",
            font=("Segoe UI", 9),
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
        ).pack(side="right")

    def _mettre_a_jour_header_connecte(self) -> None:
        """Affiche le profil connecte dans le bandeau superieur."""
        for w in self.header_user_frame.winfo_children():
            w.destroy()
        if self.current_user:
            tk.Label(
                self.header_user_frame,
                text=f"Connecté : {self.current_user.pseudo} ({self.current_user.role})",
                font=("Segoe UI", 9, "bold"),
                bg=self.COLOR_CARD,
                fg=self.COLOR_TEXT,
            ).pack(side="right")

    def deconnecter(self) -> None:
        """Deconnecte l'utilisateur et retourne a la page de connexion."""
        self.auth_service.logout()
        self.current_user = None
        self.afficher_page_connexion()

    def demarrer(self) -> None:
        """Lance la boucle principale Tkinter."""
        self.root.mainloop()


def lancer_gui() -> None:
    """Point d'entree d'execution de l'interface graphique."""
    app = QuizoraGUI()
    app.demarrer()


if __name__ == "__main__":
    lancer_gui()
