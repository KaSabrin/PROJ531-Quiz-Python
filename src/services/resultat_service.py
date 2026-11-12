"""Service métier pour l'historique des scores (US07)."""

from src.models.quiz import Quiz
from src.models.resultat import Resultat
from src.models.user import User
from src.services.storage_service import StorageService


class ResultatService:
    """Enregistre les passages de quiz et calcule l'historique d'un joueur."""

    def __init__(self, storage_service: StorageService | None = None):
        self.storage_service = storage_service or StorageService()

    def enregistrer_resultat(
        self, joueur: User, quiz: Quiz, score: int
    ) -> tuple[bool, str, Resultat | None]:
        """Ajoute un résultat à results.json.

        Un score négatif ou supérieur au barème du quiz est refusé.
        """
        score_max = quiz.total_points()
        if score_max < 1:
            return False, "Ce quiz ne contient aucune question.", None
        if score < 0 or score > score_max:
            return False, f"Score incohérent : {score} pour un barème de {score_max}.", None

        resultat = Resultat(
            id_utilisateur=joueur.id_utilisateur,
            id_quiz=quiz.id_quiz,
            score=score,
            score_max=score_max,
        )
        resultats = self.storage_service.load_results()
        resultats.append(resultat)
        if not self.storage_service.save_results(resultats):
            return False, "Impossible d'enregistrer votre score.", None
        return True, "Votre score a été enregistré.", resultat

    def historique_joueur(self, joueur: User) -> list[Resultat]:
        """Résultats du joueur uniquement, du plus récent au plus ancien."""
        mes_resultats = [
            r for r in self.storage_service.load_results()
            if r.id_utilisateur == joueur.id_utilisateur
        ]
        return sorted(mes_resultats, key=lambda r: r.date_passage, reverse=True)

    def statistiques_joueur(self, joueur: User) -> dict:
        """Nombre de quiz passés, moyenne et meilleur pourcentage."""
        historique = self.historique_joueur(joueur)
        if not historique:
            return {"nb_quiz": 0, "moyenne": 0.0, "meilleur": 0.0}
        pourcentages = [r.pourcentage for r in historique]
        return {
            "nb_quiz": len(historique),
            "moyenne": round(sum(pourcentages) / len(pourcentages), 1),
            "meilleur": round(max(pourcentages), 1),
        }
