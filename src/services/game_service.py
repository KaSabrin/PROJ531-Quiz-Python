
from src.models.quiz import Quiz
from src.models.user import User
from src.models.question import Question
from src.services.storage_service import StorageService

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


# Ajouter une question et ses réponses à un quiz

def ajouter_question_au_quiz(quiz, enonce, reponses, bonne_reponse):

    # Vérifier que la question n'est pas vide
    if not enonce.strip():
        raise ValueError("La question ne peut pas être vide.")

    # Vérifier qu'il y a au moins deux réponses
    if len(reponses) < 2:
        raise ValueError("Il faut au moins deux réponses.")

    # Vérifier qu'aucune réponse n'est vide
    if any(not reponse.strip() for reponse in reponses):
        raise ValueError("Les réponses ne peuvent pas être vides.")

    # Vérifier le numéro de la bonne réponse
    if not 1 <= bonne_reponse <= len(reponses):
        raise ValueError("Numéro de bonne réponse invalide.")

    # Créer la question
    question = Question(enonce=enonce)

    # Ajouter les réponses
    for i, texte in enumerate(reponses, start=1):
        question.ajouter_reponse(
            text_reponse=texte,
            est_correct=(i == bonne_reponse)
        )

    # Ajouter la question au quiz
    quiz.ajouter_question(question)

    return question


# T04.3 - Sauvegarder un quiz dans le fichier JSON

def sauvegarder_quiz(quiz, administrateur):

    # Vérifier les droits administrateur
    if not administrateur.is_admin():
        raise PermissionError("Accès réservé à l'administrateur.")

    # Vérifier que l'administrateur est l'auteur du quiz
    if quiz.auteur_id != administrateur.id_utilisateur:
        raise PermissionError("Vous n'êtes pas l'auteur de ce quiz.")

    # Vérifier que le quiz contient des questions
    if not quiz.questions:
        raise ValueError("Le quiz doit contenir au moins une question.")

    # Accéder au service de stockage
    stockage = StorageService()

    # Récupérer les quiz déjà enregistrés
    quiz_existants = stockage.load_quizzes()

   
    # Vérifier que le quiz n'est pas déjà enregistré
    for quiz_existant in quiz_existants:
        if quiz_existant.id_quiz == quiz.id_quiz:
            raise ValueError("Ce quiz est déjà enregistré.")

    # Ajouter le nouveau quiz
    quiz_existants.append(quiz)


    # Enregistrer tous les quiz
    if not stockage.save_quizzes(quiz_existants):
        raise OSError("Impossible de sauvegarder le quiz.")

    return True
