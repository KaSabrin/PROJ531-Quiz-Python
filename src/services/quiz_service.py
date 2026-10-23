"""Service métier pour la gestion des quiz (création, consultation, persistance)."""

from pathlib import Path
from src.models.quiz import Quiz
from src.models.question import Question
from src.models.reponse import Reponse
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.import_service import importer_quiz_depuis_txt


class QuizService:
    """Gère le cycle de vie des quiz, de leur création à leur enregistrement."""

    def __init__(self, storage_service: StorageService | None = None):
        self.storage_service = storage_service or StorageService()

    def lister_quiz(self) -> list[Quiz]:
        """Retourne la liste de tous les quiz enregistrés."""
        return self.storage_service.load_quizzes()

    def get_quiz_par_id(self, id_quiz: str) -> Quiz | None:
        """Recherche un quiz par son identifiant unique."""
        quizzes = self.lister_quiz()
        for q in quizzes:
            if q.id_quiz == id_quiz:
                return q
        return None

    def creer_quiz_manuel(
        self,
        titre: str,
        description: str,
        auteur: User,
        questions_data: list[dict],
    ) -> tuple[bool, str, Quiz | None]:
        """Crée et sauvegarde un quiz avec ses questions et réponses."""

        # Vérifier les droits administrateur
        if not auteur.is_admin():
            return False, "Accès réservé à l'administrateur.", None

        # Vérifier le titre
        titre = titre.strip()
        if not titre:
            return False, "Le titre du quiz est obligatoire.", None

        # Vérifier la présence des questions
        if not questions_data:
            return False, "Le quiz doit contenir au moins une question.", None

        # Créer le quiz
        quiz = Quiz(
            titre=titre,
            description=description.strip(),
            auteur_id=auteur.id_utilisateur
        )

        # Ajouter les questions
        for numero, q_dict in enumerate(questions_data, start=1):
            enonce = q_dict.get("enonce", "").strip()

            if not enonce:
                return False, f"La question {numero} est vide.", None

            # Vérifier les points
            try:
                points = int(q_dict.get("points", 1))
            except (ValueError, TypeError):
                return False, "Nombre de points invalide.", None

            if points < 1:
                return False, "Les points doivent être positifs.", None

            question = Question(enonce=enonce, points=points)

            reponses_list = q_dict.get("reponses", [])

            # Vérifier le nombre de réponses
            if len(reponses_list) < 2:
                return False, "Il faut au moins deux réponses.", None

            # Ajouter les réponses
            for rep_dict in reponses_list:
                texte = rep_dict.get("texte", "").strip()

                if not texte:
                    return False, "Une réponse ne peut pas être vide.", None

                question.ajouter_reponse(
                    text_reponse=texte,
                    est_correct=bool(rep_dict.get("est_correct", False))
                )

            # Vérifier qu'il y a exactement une bonne réponse
            if len(question.get_bonnes_reponses()) != 1:
                return False, "Il faut exactement une bonne réponse par question.", None

            quiz.ajouter_question(question)

        # Récupérer les quiz enregistrés
        quizzes = self.storage_service.load_quizzes()

        # Éviter un doublon d'identifiant
        for quiz_existant in quizzes:
            if quiz_existant.id_quiz == quiz.id_quiz:
                return False, "Ce quiz existe déjà.", None

        # Ajouter et enregistrer le quiz
        quizzes.append(quiz)

        if not self.storage_service.save_quizzes(quizzes):
            return False, "Erreur lors de la sauvegarde du quiz.", None

        return (
            True,
            f"Quiz '{quiz.titre}' créé avec succès ({len(quiz.questions)} questions).",
            quiz
        )


    def importer_quiz_depuis_fichier(
        self,
        chemin_fichier: str | Path,
        auteur: User,
    ) -> tuple[bool, str, Quiz | None]:
        """
        Importe un quiz à partir d'un fichier texte (.txt) en utilisant le parseur d'import.
        """
        if not auteur.is_admin():
            return False, "Accès refusé : seul un administrateur peut importer un quiz.", None

        donnees_quiz = importer_quiz_depuis_txt(chemin_fichier)
        if not donnees_quiz:
            return False, "Fichier introuvable ou erreur de lecture.", None

        titre = donnees_quiz.get("titre", "").strip()
        if not titre:
            return False, "Le fichier ne contient pas de TITRE valide.", None

        questions_brutes = donnees_quiz.get("questions", [])
        if not questions_brutes:
            return False, "Aucune question trouvée dans le fichier.", None

        questions_data = []
        for q in questions_brutes:
            reponses = []
            for opt in q.get("options", []):
                reponses.append({
                    "texte": opt.get("texte", ""),
                    "est_correct": opt.get("est_correcte", False),
                })
            questions_data.append({
                "enonce": q.get("enonce", ""),
                "points": q.get("points", 1),
                "reponses": reponses,
            })

        return self.creer_quiz_manuel(
            titre=titre,
            description=donnees_quiz.get("description", ""),
            auteur=auteur,
            questions_data=questions_data,
        )
