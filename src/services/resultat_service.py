"""Service métier pour l'enregistrement et la consultation des résultats (Sprint 4 - US07)."""

from src.models.quiz import Quiz
from src.models.resultat import Resultat
from src.models.user import User
from src.services.storage_service import StorageService


class ResultatService:
    """Gère la sauvegarde des scores et l'historique personnel des joueurs."""

    def __init__(self, storage_service: StorageService | None = None):
        self.storage_service = storage_service or StorageService()

    def enregistrer_resultat(
        self,
        joueur: User,
        quiz: Quiz,
        score: int,
    ) -> tuple[bool, str, Resultat | None]:
        """Crée un résultat pour un passage de quiz et l'ajoute à results.json."""
        if score < 0 or score > quiz.total_points():
            return False, "Score incohérent avec le barème du quiz.", None

        resultat = Resultat(
            id_utilisateur=joueur.id_utilisateur,
            id_quiz=quiz.id_quiz,
            score=score,
            score_max=quiz.total_points(),
        )

        resultats = self.storage_service.load_results()
        resultats.append(resultat)

        if not self.storage_service.save_results(resultats):
            return False, "Erreur lors de la sauvegarde du résultat.", None

        return True, "Résultat enregistré dans votre historique.", resultat

    def historique_joueur(self, joueur: User) -> list[Resultat]:
        """Retourne les résultats d'un joueur, du plus récent au plus ancien."""
        resultats = [
            r for r in self.storage_service.load_results()
            if r.id_utilisateur == joueur.id_utilisateur
        ]
        return sorted(resultats, key=lambda r: r.date_passage, reverse=True)

    def statistiques_joueur(self, joueur: User) -> dict:
        """Calcule le nombre de quiz passés, la moyenne et le meilleur pourcentage."""
        resultats = self.historique_joueur(joueur)
        if not resultats:
            return {"nb_passages": 0, "moyenne": 0.0, "meilleur": 0.0}

        pourcentages = [r.pourcentage for r in resultats]
        return {
            "nb_passages": len(resultats),
            "moyenne": round(sum(pourcentages) / len(pourcentages), 1),
            "meilleur": max(pourcentages),
        }
