"""Modèle de données représentant le Résultat d'un passage de quiz."""

from datetime import datetime
import uuid


class Resultat:
    """Classe représentant le résultat obtenu par un utilisateur à un quiz."""

    def __init__(
        self,
        id_utilisateur: str,
        id_quiz: str,
        score: int,
        score_max: int,
        id_resultat: str | None = None,
        date_passage: str | None = None,
    ):
        self.id_resultat = id_resultat or str(uuid.uuid4())
        self.id_utilisateur = id_utilisateur
        self.id_quiz = id_quiz
        self.score = int(score)
        self.score_max = max(1, int(score_max))
        self.date_passage = date_passage or datetime.now().isoformat()

    @property
    def pourcentage(self) -> float:
        """Calcule le pourcentage de réussite."""
        return round((self.score / self.score_max) * 100, 2)

    def to_dict(self) -> dict:
        """Convertit le résultat en dictionnaire sérialisable."""
        return {
            "id_resultat": self.id_resultat,
            "id_utilisateur": self.id_utilisateur,
            "id_quiz": self.id_quiz,
            "score": self.score,
            "score_max": self.score_max,
            "date_passage": self.date_passage,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Resultat":
        """Instancie un Résultat à partir d'un dictionnaire."""
        return cls(
            id_resultat=data.get("id_resultat"),
            id_utilisateur=data.get("id_utilisateur", ""),
            id_quiz=data.get("id_quiz", ""),
            score=data.get("score", 0),
            score_max=data.get("score_max", 1),
            date_passage=data.get("date_passage"),
        )

    def __repr__(self) -> str:
        return f"<Resultat user={self.id_utilisateur} score={self.score}/{self.score_max}>"
