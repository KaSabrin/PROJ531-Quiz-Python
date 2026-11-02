import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from src.services.import_service import importer_quiz_depuis_txt

class TestImportQuiz(unittest.TestCase):
    
    def setUp(self):
        self.test_filename = "temp_quiz_test.txt"
        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write("TITRE: Quiz Mathématiques\n")
            f.write("DESCRIPTION: Test des fonctions de calcul\n\n")
            f.write("QUESTION: Combien font 2 + 2 ? [2 pts]\n")
            f.write("- 3\n")
            f.write("* 4\n")
            f.write("- 5\n")

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_import_reussi(self):
        quiz = importer_quiz_depuis_txt(self.test_filename)
        self.assertIsNotNone(quiz)
        self.assertEqual(quiz["titre"], "Quiz Mathématiques")
        self.assertEqual(len(quiz["questions"]), 1)
        self.assertTrue(quiz["questions"][0]["options"][1]["est_correcte"])

    def test_fichier_inexistant(self):
        quiz = importer_quiz_depuis_txt("inexistant.txt")
        self.assertIsNone(quiz)

if __name__ == "__main__":
    unittest.main()
