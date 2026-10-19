"""Modèle de données représentant un Utilisateur."""

from datetime import datetime
import uuid


class User:
    """Classe représentant un compte utilisateur (joueur ou administrateur)."""

    ROLE_JOUEUR = "joueur"
    ROLE_ADMIN = "admin"

    def __init__(
        self,
        pseudo: str,
        email: str,
        mdp_hash: str,
        role: str = ROLE_JOUEUR,
        id_utilisateur: str | None = None,
        date_creation: str | None = None,
    ):
        self.id_utilisateur = id_utilisateur or str(uuid.uuid4())
        self.pseudo = pseudo.strip()
        self.email = email.strip().lower()
        self.mdp_hash = mdp_hash
        self.role = role if role in (self.ROLE_JOUEUR, self.ROLE_ADMIN) else self.ROLE_JOUEUR
        self.date_creation = date_creation or datetime.now().isoformat()

    def is_admin(self) -> bool:
        """Indique si l'utilisateur possède les droits administrateur."""
        return self.role == self.ROLE_ADMIN

    def to_dict(self) -> dict:
        """Sérialise l'objet utilisateur en dictionnaire JSON-compatible."""
        return {
            "id_utilisateur": self.id_utilisateur,
            "pseudo": self.pseudo,
            "email": self.email,
            "mdp_hash": self.mdp_hash,
            "role": self.role,
            "date_creation": self.date_creation,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Reconstruit une instance User depuis un dictionnaire."""
        return cls(
            id_utilisateur=data.get("id_utilisateur"),
            pseudo=data.get("pseudo", ""),
            email=data.get("email", ""),
            mdp_hash=data.get("mdp_hash", ""),
            role=data.get("role", cls.ROLE_JOUEUR),
            date_creation=data.get("date_creation"),
        )

    def __repr__(self) -> str:
        return f"<User pseudo={self.pseudo!r} role={self.role!r} email={self.email!r}>"
