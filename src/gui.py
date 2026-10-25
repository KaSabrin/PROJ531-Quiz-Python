"""Interface graphique (GUI) moderne pour l'application Quizora avec Tkinter.

Fournit une page de connexion graphique, une page d'inscription et un tableau
de bord adapte au role de l'utilisateur (Joueur / Administrateur).
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from src.models.user import User
from src.services.auth_service import AuthService
from src.services.quiz_service import QuizService
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
            text="Connexion a votre compte",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        )
        lbl_titre.pack(pady=(25, 4))

        lbl_desc = tk.Label(
            card,
            text="Entrez vos identifiants pour acceder a l'espace Quizora",
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
                lbl_feedback.config(text="[OK] Connexion reussie !", fg=self.COLOR_SUCCESS)
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
            text="Creer un nouveau compte",
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
            text="Inscription a Quizora",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
        )
        lbl_titre.pack(pady=(20, 2))

        lbl_desc = tk.Label(
            card,
            text="Creez votre compte pour participer aux quiz",
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
            text="Pseudo (3 a 20 caracteres) :",
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
            text="Mot de passe (min. 6 car. + 1 chiffre) :",
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
                    text="[OK] Inscription validee ! Redirection vers la connexion...",
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
            text="< Retour a la connexion",
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
        add_info_row("Role", self.current_user.role.capitalize())
        add_info_row("Identifiant unique", self.current_user.id_utilisateur[:13] + "...")
        add_info_row("Date de creation", self.current_user.date_creation[:19])

        btn_deconnexion = tk.Button(
            carte_profil,
            text="Se deconnecter",
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

        # Liste deroulante des quiz
        list_container = tk.Frame(carte_principale, bg=self.COLOR_CARD)
        list_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        canvas = tk.Canvas(list_container, bg=self.COLOR_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLOR_CARD)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
                    text=f"{len(q.questions)} questions | {q.total_points()} points | {desc}",
                    font=("Segoe UI", 8),
                    bg=self.COLOR_BORDER,
                    fg=self.COLOR_MUTED,
                    anchor="w",
                ).pack(fill="x")

    def _mettre_a_jour_header_deconnecte(self) -> None:
        """Nettoie les informations du bandeau quand aucun utilisateur n'est connecte."""
        for w in self.header_user_frame.winfo_children():
            w.destroy()
        tk.Label(
            self.header_user_frame,
            text="Non connecte",
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
                text=f"Connecte : {self.current_user.pseudo} ({self.current_user.role})",
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
