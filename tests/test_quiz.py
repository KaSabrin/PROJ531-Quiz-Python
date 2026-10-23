"""Tests unitaires pour la gestion et la création des quiz (QuizService)."""

import unittest
import tempfile
import shutil
from pathlib import Path
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.quiz_service import QuizService


class TestQuizService(unittest.TestCase):
    """Vérifie la création manuelle et l'importation de quiz."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_service = StorageService(data_dir=self.test_dir)
        self.quiz_service = QuizService(storage_service=self.storage_service)

        self.admin = User(
            pseudo="admin_test",
            email="admin@test.fr",
            mdp_hash="hash123",
            role=User.ROLE_ADMIN,
        )
        self.joueur = User(
            pseudo="joueur_test",
            email="joueur@test.fr",
            mdp_hash="hash456",
            role=User.ROLE_JOUEUR,
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_creer_quiz_manuel_succes(self):
        """Vérifie la création d'un quiz complet par un administrateur."""
        questions_data = [
            {
                "enonce": "Quelle est la capitale de la France ?",
                "points": 2,
                "reponses": [
                    {"texte": "Lyon", "est_correct": False},
                    {"texte": "Paris", "est_correct": True},
                ],
            }
        ]
        succes, message, quiz = self.quiz_service.creer_quiz_manuel(
            titre="Géographie",
            description="Test de géographie",
            auteur=self.admin,
            questions_data=questions_data,
        )
        self.assertTrue(succes)
        self.assertIsNotNone(quiz)
        self.assertEqual(quiz.titre, "Géographie")
        self.assertEqual(len(quiz.questions), 1)
        self.assertEqual(quiz.total_points(), 2)

        # Vérifier persistance
        quizzes = self.storage_service.load_quizzes()
        self.assertEqual(len(quizzes), 1)
        self.assertEqual(quizzes[0].titre, "Géographie")

    def test_creer_quiz_interdit_pour_joueur(self):
        """Vérifie qu'un joueur simple ne peut pas créer de quiz."""
        questions_data = [{"enonce": "Question", "points": 1, "reponses": [{"texte": "A", "est_correct": True}, {"texte": "B", "est_correct": False}]}]
        succes, message, quiz = self.quiz_service.creer_quiz_manuel(
            titre="Quiz Interdit",
            description="",
            auteur=self.joueur,
            questions_data=questions_data,
        )
        self.assertFalse(succes)
        self.assertIn("seul un administrateur", message.lower())

    def test_creer_quiz_sans_titre(self):
        """Vérifie le rejet d'un quiz avec un titre vide."""
        questions_data = [{"enonce": "Question", "points": 1, "reponses": [{"texte": "A", "est_correct": True}, {"texte": "B", "est_correct": False}]}]
        succes, message, quiz = self.quiz_service.creer_quiz_manuel(
            titre="   ",
            description="",
            auteur=self.admin,
            questions_data=questions_data,
        )
        self.assertFalse(succes)
        self.assertIn("titre", message.lower())

    def test_importer_quiz_depuis_fichier(self):
        """Vérifie l'import automatique à partir d'un fichier texte."""
        fichier_test = Path(self.test_dir) / "quiz_import.txt"
        fichier_test.write_text(
            "TITRE: Python Test\n"
            "DESCRIPTION: Un quiz de test\n\n"
            "QUESTION: Python est-il interprété ? [3 pts]\n"
            "* Oui\n"
            "- Non\n",
            encoding="utf-8"
        )

        succes, message, quiz = self.quiz_service.importer_quiz_depuis_fichier(fichier_test, auteur=self.admin)
        self.assertTrue(succes)
        self.assertIsNotNone(quiz)
        self.assertEqual(quiz.titre, "Python Test")
        self.assertEqual(quiz.total_points(), 3)
        self.assertEqual(len(quiz.questions[0].reponses), 2)


if __name__ == "__main__":
    unittest.main()
