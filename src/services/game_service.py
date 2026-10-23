
from src.models.quiz import Quiz
from src.models.user import User


def creer_quiz(titre, description, administrateur):
    # Vérifier les droits administrateur
    if not administrateur.is_admin():
        raise PermissionError("Accès réservé à l'administrateur.")

    # Vérifier le titre
    if not titre.strip():
        raise ValueError("Le titre du quiz est obligatoire.")

    # Créer le quiz
    quiz = Quiz(
        titre=titre,
        description=description,
        auteur_id=administrateur.id_utilisateur
    )

    return quiz

