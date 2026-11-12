"""Tests unitaires de l'historique des scores (ResultatService)."""

import tempfile
import unittest

from src.models.question import Question
from src.models.quiz import Quiz
from src.models.resultat import Resultat
from src.models.user import User
from src.services.resultat_service import ResultatService
from src.services.storage_service import StorageService


def creer_quiz(titre: str = "Quiz test", points=(2, 1, 1)) -> Quiz:
    quiz = Quiz(titre=titre)
    for i, pts in enumerate(points, 1):
        q = Question(enonce=f"Question {i}", points=pts)
        q.ajouter_reponse("Bonne", est_correct=True)
        q.ajouter_reponse("Mauvaise")
        quiz.ajouter_question(q)
    return quiz


class TestResultatService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageService(data_dir=self.temp_dir.name)
        self.service = ResultatService(storage_service=self.storage)
        self.alice = User(pseudo="alice", email="alice@test.fr", mdp_hash="h1")
        self.bob = User(pseudo="bob", email="bob@test.fr", mdp_hash="h2")
        self.quiz = creer_quiz()  # barème total : 4 points

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_enregistrement_persiste_dans_results_json(self):
        succes, _, resultat = self.service.enregistrer_resultat(self.alice, self.quiz, 3)
        self.assertTrue(succes)
        # Relecture depuis le disque avec une nouvelle instance de stockage
        relu = StorageService(data_dir=self.temp_dir.name).load_results()
        self.assertEqual(len(relu), 1)
        self.assertEqual(relu[0].id_resultat, resultat.id_resultat)
        self.assertEqual((relu[0].score, relu[0].score_max), (3, 4))
        self.assertEqual(relu[0].id_quiz, self.quiz.id_quiz)

    def test_rejet_des_scores_incoherents(self):
        for score in (-1, 5):
            succes, message, resultat = self.service.enregistrer_resultat(self.alice, self.quiz, score)
            self.assertFalse(succes, f"le score {score} aurait dû être refusé")
            self.assertIsNone(resultat)
        self.assertEqual(self.storage.load_results(), [])

    def test_rejet_d_un_quiz_vide(self):
        succes, _, _ = self.service.enregistrer_resultat(self.alice, Quiz(titre="Vide"), 0)
        self.assertFalse(succes)
        self.assertEqual(self.storage.load_results(), [])

    def test_historique_filtre_par_joueur_et_trie(self):
        self.service.enregistrer_resultat(self.alice, self.quiz, 4)
        self.service.enregistrer_resultat(self.bob, self.quiz, 1)
        self.service.enregistrer_resultat(self.alice, self.quiz, 2)
        # Dates forcées pour ne pas dépendre de la résolution de l'horloge
        resultats = self.storage.load_results()
        for i, r in enumerate(resultats):
            r.date_passage = f"2026-11-02T10:0{i}:00"
        self.storage.save_results(resultats)

        historique = self.service.historique_joueur(self.alice)
        self.assertEqual(len(historique), 2)
        self.assertTrue(all(r.id_utilisateur == self.alice.id_utilisateur for r in historique))
        self.assertEqual([r.score for r in historique], [2, 4])  # du plus récent au plus ancien
        self.assertEqual(len(self.service.historique_joueur(self.bob)), 1)

    def test_statistiques(self):
        self.service.enregistrer_resultat(self.alice, self.quiz, 4)  # 100 %
        self.service.enregistrer_resultat(self.alice, self.quiz, 3)  # 75 %
        stats = self.service.statistiques_joueur(self.alice)
        self.assertEqual(stats["nb_quiz"], 2)
        self.assertEqual(stats["moyenne"], 87.5)
        self.assertEqual(stats["meilleur"], 100.0)
        self.assertEqual(self.service.statistiques_joueur(self.bob),
                         {"nb_quiz": 0, "moyenne": 0.0, "meilleur": 0.0})


    def test_moyenne_et_meilleur_arrondis_pareil(self):
        """Moyenne et meilleur score sont tous deux arrondis à une décimale (3/7 = 42.9 %)."""
        self.storage.save_results([Resultat(self.alice.id_utilisateur, "q1", 3, 7)])
        stats = self.service.statistiques_joueur(self.alice)
        self.assertEqual(stats["moyenne"], 42.9)
        self.assertEqual(stats["meilleur"], 42.9)

if __name__ == "__main__":
    unittest.main()
