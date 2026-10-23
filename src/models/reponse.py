"""Modèle de données représentant une proposition de Réponse."""

import uuid


class Reponse:
    """Classe représentant une proposition de réponse associée à une question."""

    def __init__(
        self,
        text_reponse: str,
        est_correct: bool = False,
        id_reponse: str | None = None,
        id_question: str | None = None,
    ):
        self.id_reponse = id_reponse or str(uuid.uuid4())
        self.id_question = id_question
        self.text_reponse = text_reponse.strip()
        self.est_correct = bool(est_correct)

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire sérialisable."""
        return {
            "id_reponse": self.id_reponse,
            "id_question": self.id_question,
            "text_reponse": self.text_reponse,
            "est_correct": self.est_correct,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reponse":
        """Instancie une Réponse à partir d'un dictionnaire."""
        return cls(
            id_reponse=data.get("id_reponse"),
            id_question=data.get("id_question"),
            text_reponse=data.get("text_reponse", ""),
            est_correct=data.get("est_correct", False),
        )

    def __repr__(self) -> str:
        return f"<Reponse {self.text_reponse!r} correct={self.est_correct}>"
