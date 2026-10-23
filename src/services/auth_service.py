"""Service d'authentification : Inscription, connexion, validation et sessions."""

from src.models.user import User
from src.services.storage_service import StorageService
from src.security import hash_password, verify_password
from src.utils.validators import validate_email, validate_password, validate_pseudo


class AuthService:
    """Gère la logique métier liée aux comptes utilisateurs et à l'authentification."""

    def __init__(self, storage_service: StorageService | None = None):
        self.storage = storage_service or StorageService()
        self.current_user: User | None = None
        self._ensure_default_accounts()

    def _ensure_default_accounts(self) -> None:
        """Initialise un compte administrateur et un joueur de démonstration si la base est vide."""
        users = self.storage.load_users()
        if not users:
            # Création du compte administrateur par défaut
            admin_user = User(
                pseudo="admin",
                email="admin@quiz.fr",
                mdp_hash=hash_password("Admin123!"),
                role=User.ROLE_ADMIN,
            )
            # Création d'un joueur par défaut
            joueur_user = User(
                pseudo="joueur1",
                email="joueur1@quiz.fr",
                mdp_hash=hash_password("Joueur123!"),
                role=User.ROLE_JOUEUR,
            )
            self.storage.save_users([admin_user, joueur_user])

    def register(
        self,
        pseudo: str,
        email: str,
        password: str,
        role: str = User.ROLE_JOUEUR,
    ) -> tuple[bool, str, User | None]:
        """Inscrit un nouvel utilisateur après validation stricte des données.

        Returns:
            Tuple (succès: bool, message: str, utilisateur: User | None)
        """
        # 1. Validation du pseudo
        valid_pseudo, msg_pseudo = validate_pseudo(pseudo)
        if not valid_pseudo:
            return False, msg_pseudo, None

        # 2. Validation de l'email
        if not validate_email(email):
            return False, "Format d'adresse e-mail invalide.", None

        # 3. Validation du mot de passe
        valid_pwd, msg_pwd = validate_password(password)
        if not valid_pwd:
            return False, msg_pwd, None

        # 4. Vérification d'unicité (pseudo et email)
        users = self.storage.load_users()
        clean_pseudo = pseudo.strip().lower()
        clean_email = email.strip().lower()

        for u in users:
            if u.pseudo.lower() == clean_pseudo:
                return False, f"Le pseudo '{pseudo}' est déjà utilisé.", None
            if u.email.lower() == clean_email:
                return False, f"L'adresse e-mail '{email}' est déjà enregistrée.", None

        # 5. Hachage sécurisé du mot de passe
        mdp_hash = hash_password(password)

        # 6. Création et sauvegarde
        new_user = User(
            pseudo=pseudo.strip(),
            email=clean_email,
            mdp_hash=mdp_hash,
            role=role,
        )
        users.append(new_user)
        self.storage.save_users(users)

        return True, "Inscription réussie !", new_user

    def login(self, identifier: str, password: str) -> tuple[bool, str, User | None]:
        """Connecte un utilisateur par son pseudo OU son e-mail.

        Returns:
            Tuple (succès: bool, message: str, utilisateur: User | None)
        """
        if not identifier or not password:
            return False, "Identifiant et mot de passe requis.", None

        clean_id = identifier.strip().lower()
        users = self.storage.load_users()

        target_user: User | None = None
        for u in users:
            if u.pseudo.lower() == clean_id or u.email.lower() == clean_id:
                target_user = u
                break

        if target_user is None:
            return False, "Identifiant ou mot de passe incorrect.", None

        # Vérification cryptographique du mot de passe
        if not verify_password(password, target_user.mdp_hash):
            return False, "Identifiant ou mot de passe incorrect.", None

        self.current_user = target_user
        return True, f"Connexion réussie. Bienvenue, {target_user.pseudo} !", target_user

    def logout(self) -> None:
        """Déconnecte l'utilisateur courant."""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """Vérifie si un utilisateur est actuellement connecté."""
        return self.current_user is not None

    def get_current_user(self) -> User | None:
        """Retourne l'utilisateur connecté."""
        return self.current_user

    def list_users(self) -> list[User]:
        """Retourne la liste complète des utilisateurs enregistrés."""
        return self.storage.load_users()

    def get_user_by_id(self, user_id: str) -> User | None:
        """Recherche un utilisateur par son identifiant unique."""
        for u in self.storage.load_users():
            if u.id_utilisateur == user_id:
                return u
        return None
