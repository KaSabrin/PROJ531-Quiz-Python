import unittest
from unittest.mock import Mock, patch
from io import StringIO

from src.cli import QuizAppCLI
from src.models.quiz import Quiz
from src.models.question import Question
from src.models.user import User


class TestQuizCLI(unittest.TestCase):

    def setUp(self):
        self.app = QuizAppCLI.__new__(QuizAppCLI)
        self.app.quiz_service = Mock()
        self.app.resultat_service = Mock()

        self.joueur = User(
            "joueur_test", "joueur@test.fr", "hash_test"
        )

    def test_refuser_questions_invalides(self):
        # Tester plusieurs types de questions invalides
        cas = [[], [True], [False, False], [True, True]]

        for bonnes in cas:
            with self.subTest(reponses=bonnes):
                question = Question("Question de test")

                for i, correcte in enumerate(bonnes):
                    question.ajouter_reponse(
                        f"Réponse {i + 1}", correcte
                    )

                quiz = Quiz(
                    "Quiz invalide", questions=[question]
                )

                self.app.quiz_service.lister_quiz.return_value = [quiz]

                with patch("builtins.input", side_effect=["1", ""]), \
                     patch("sys.stdout", new_callable=StringIO) as sortie:
                    self.app.action_passer_quiz(self.joueur)

                self.assertIn(
                    "Quiz invalide", sortie.getvalue()
                )

                self.app.resultat_service.enregistrer_resultat.assert_not_called()

    def test_quiz_valide(self):
        question = Question("Combien font 2 + 2 ?")
        question.ajouter_reponse("3", False)
        question.ajouter_reponse("4", True)

        quiz = Quiz("Quiz valide", questions=[question])

        self.app.quiz_service.lister_quiz.return_value = [quiz]

        self.app.resultat_service.enregistrer_resultat.return_value = (
            True, "Score enregistré", None
        )

        with patch("builtins.input", side_effect=["1", "2", ""]), \
             patch("sys.stdout", new_callable=StringIO) as sortie:
            self.app.action_passer_quiz(self.joueur)

        self.assertIn("FIN DU QUIZ", sortie.getvalue())

        self.app.resultat_service.enregistrer_resultat.assert_called_once_with(
            self.joueur, quiz, 1
        )


if __name__ == "__main__":
    unittest.main()