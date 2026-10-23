"""Modèle de données représentant une Question d'un quiz."""

import uuid
from src.models.reponse import Reponse


class Question:
    """Classe représentant une question appartenant à un quiz."""

    def __init__(
        self,
        enonce: str,
        reponses: list[Reponse] | None = None,
        points: int = 1,
        id_question: str | None = None,
        id_quiz: str | None = None,
    ):
        self.id_question = id_question or str(uuid.uuid4())
        self.id_quiz = id_quiz
        self.enonce = enonce.strip()
        self.points = max(1, int(points))
        self.reponses: list[Reponse] = reponses or []

    def ajouter_reponse(self, text_reponse: str, est_correct: bool = False) -> Reponse:
        """Ajoute une proposition de réponse à la question."""
        rep = Reponse(
            text_reponse=text_reponse,
            est_correct=est_correct,
            id_question=self.id_question,
        )
        self.reponses.append(rep)
        return rep

    def get_bonnes_reponses(self) -> list[Reponse]:
        """Retourne la liste des réponses correctes."""
        return [r for r in self.reponses if r.est_correct]

    def to_dict(self) -> dict:
        """Convertit la question et ses propositions de réponses en dictionnaire."""
        return {
            "id_question": self.id_question,
            "id_quiz": self.id_quiz,
            "enonce": self.enonce,
            "points": self.points,
            "reponses": [r.to_dict() for r in self.reponses],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """Instancie une Question et ses réponses à partir d'un dictionnaire."""
        reponses = [Reponse.from_dict(r) for r in data.get("reponses", [])]
        return cls(
            id_question=data.get("id_question"),
            id_quiz=data.get("id_quiz"),
            enonce=data.get("enonce", ""),
            points=data.get("points", 1),
            reponses=reponses,
        )

    def __repr__(self) -> str:
        return f"<Question {self.enonce!r} ({len(self.reponses)} réponses)>"
