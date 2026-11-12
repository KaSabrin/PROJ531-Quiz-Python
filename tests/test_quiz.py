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

    def test_quiz_de_demonstration_importes_au_nom_de_l_admin(self):
        """Au premier lancement, les quiz du dossier exemples/ sont créés par l'administrateur."""
        self.storage_service.save_users([self.admin, self.joueur])
        quizzes = QuizService(storage_service=self.storage_service).lister_quiz()
        self.assertEqual(len(quizzes), 3)
        self.assertTrue(all(q.auteur_id == self.admin.id_utilisateur for q in quizzes))
        self.assertTrue(all(len(q.questions) == 5 for q in quizzes))

    def test_quiz_de_demonstration_non_reimportes(self):
        """Les quiz d'exemple ne sont pas ajoutés une seconde fois au lancement suivant."""
        self.storage_service.save_users([self.admin])
        QuizService(storage_service=self.storage_service)
        QuizService(storage_service=self.storage_service)
        self.assertEqual(len(self.storage_service.load_quizzes()), 3)


    def test_titre_en_double_refuse(self):
        """Importer deux fois le même fichier ne crée pas de doublon dans le catalogue."""
        fichier = Path(__file__).resolve().parent.parent / "exemples" / "quiz_python.txt"
        premier, _, _ = self.quiz_service.importer_quiz_depuis_fichier(fichier, auteur=self.admin)
        second, message, _ = self.quiz_service.importer_quiz_depuis_fichier(fichier, auteur=self.admin)
        self.assertTrue(premier)
        self.assertFalse(second)
        self.assertIn("existe déjà", message)
        self.assertEqual(len(self.storage_service.load_quizzes()), 1)

if __name__ == "__main__":
    unittest.main()
