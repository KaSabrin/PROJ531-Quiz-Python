"""Modèle de données représentant un Quiz complet."""

from datetime import datetime
import uuid
from src.models.question import Question


class Quiz:
    """Classe représentant un quiz contenant une série de questions."""

    def __init__(
        self,
        titre: str,
        description: str = "",
        auteur_id: str | None = None,
        questions: list[Question] | None = None,
        id_quiz: str | None = None,
        date_creation: str | None = None,
    ):
        self.id_quiz = id_quiz or str(uuid.uuid4())
        self.titre = titre.strip()
        self.description = description.strip()
        self.auteur_id = auteur_id
        self.questions: list[Question] = questions or []
        self.date_creation = date_creation or datetime.now().isoformat()

    def ajouter_question(self, question: Question) -> None:
        """Ajoute une question au quiz en synchronisant l'identifiant du quiz."""
        question.id_quiz = self.id_quiz
        self.questions.append(question)

    def total_points(self) -> int:
        """Calcule le nombre total maximal de points pour ce quiz."""
        return sum(q.points for q in self.questions)

    def to_dict(self) -> dict:
        """Convertit le quiz et ses questions associées en dictionnaire."""
        return {
            "id_quiz": self.id_quiz,
            "titre": self.titre,
            "description": self.description,
            "auteur_id": self.auteur_id,
            "date_creation": self.date_creation,
            "questions": [q.to_dict() for q in self.questions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """Instancie un Quiz complet à partir d'un dictionnaire."""
        questions = [Question.from_dict(q) for q in data.get("questions", [])]
        return cls(
            id_quiz=data.get("id_quiz"),
            titre=data.get("titre", ""),
            description=data.get("description", ""),
            auteur_id=data.get("auteur_id"),
            date_creation=data.get("date_creation"),
            questions=questions,
        )

    def __repr__(self) -> str:
        return f"<Quiz {self.titre!r} ({len(self.questions)} questions)>"
