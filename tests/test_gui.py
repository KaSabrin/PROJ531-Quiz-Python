
import unittest
from unittest.mock import Mock, patch

from src.gui import QuizoraGUI
from src.models.quiz import Quiz
from src.models.question import Question


class TestQuizGUI(unittest.TestCase):

    def setUp(self):
        self.app = QuizoraGUI.__new__(QuizoraGUI)
        self.app._nettoyer_contenu = Mock()
        self.app.resultat_service = Mock()

    def test_refuser_quiz_vide(self):
        quiz = Quiz("Quiz vide", questions=[])

        with patch("src.gui.messagebox.showwarning") as avertissement:
            self.app.afficher_page_passage(quiz)

        avertissement.assert_called_once()
        self.assertIn("aucune question", avertissement.call_args.args[1])
        self.app._nettoyer_contenu.assert_not_called()
        self.app.resultat_service.enregistrer_resultat.assert_not_called()

    def test_refuser_questions_invalides(self):
        cas = [[], [True], [False, False], [True, True]]

        for bonnes in cas:
            with self.subTest(reponses=bonnes):
                question = Question("Question de test")

                for i, correcte in enumerate(bonnes):
                    question.ajouter_reponse(
                        f"Réponse {i + 1}", correcte
                    )

                quiz = Quiz("Quiz invalide", questions=[question])

                with patch("src.gui.messagebox.showwarning") as avertissement:
                    self.app.afficher_page_passage(quiz)

                avertissement.assert_called_once()
                self.assertIn("Quiz invalide", avertissement.call_args.args[1])
                self.app._nettoyer_contenu.assert_not_called()
                self.app.resultat_service.enregistrer_resultat.assert_not_called()


if __name__ == "__main__":
    unittest.main()
