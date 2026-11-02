"""Tests unitaires pour la sauvegarde des résultats et l'historique (Sprint 4 - US07)."""

import unittest
import tempfile
import shutil
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.quiz_service import QuizService
from src.services.resultat_service import ResultatService


class TestResultatService(unittest.TestCase):
    """Vérifie l'enregistrement des scores et le calcul de l'historique."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_service = StorageService(data_dir=self.test_dir)
        self.quiz_service = QuizService(storage_service=self.storage_service)
        self.resultat_service = ResultatService(storage_service=self.storage_service)

        admin = User(pseudo="admin_test", email="admin@test.fr", mdp_hash="h", role=User.ROLE_ADMIN)
        self.joueur = User(pseudo="joueur_a", email="a@test.fr", mdp_hash="h", role=User.ROLE_JOUEUR)
        self.autre_joueur = User(pseudo="joueur_b", email="b@test.fr", mdp_hash="h", role=User.ROLE_JOUEUR)

        _, _, self.quiz = self.quiz_service.creer_quiz_manuel(
            titre="Quiz de test",
            description="",
            auteur=admin,
            questions_data=[
                {
                    "enonce": "2 + 2 ?",
                    "points": 2,
                    "reponses": [
                        {"texte": "4", "est_correct": True},
                        {"texte": "5", "est_correct": False},
                    ],
                },
                {
                    "enonce": "Capitale de l'Italie ?",
                    "points": 2,
                    "reponses": [
                        {"texte": "Rome", "est_correct": True},
                        {"texte": "Milan", "est_correct": False},
                    ],
                },
            ],
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_enregistrer_resultat_persiste(self):
        """Vérifie que le résultat est bien écrit dans results.json."""
        succes, _, resultat = self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 3)
        self.assertTrue(succes)
        self.assertEqual(resultat.score_max, 4)
        self.assertEqual(resultat.pourcentage, 75.0)

        recharges = StorageService(data_dir=self.test_dir).load_results()
        self.assertEqual(len(recharges), 1)
        self.assertEqual(recharges[0].id_quiz, self.quiz.id_quiz)

    def test_score_incoherent_rejete(self):
        """Vérifie le rejet d'un score négatif ou supérieur au barème."""
        self.assertFalse(self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 5)[0])
        self.assertFalse(self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, -1)[0])
        self.assertEqual(self.storage_service.load_results(), [])

    def test_historique_filtre_par_joueur(self):
        """Vérifie qu'un joueur ne voit que ses propres résultats."""
        self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 4)
        self.resultat_service.enregistrer_resultat(self.autre_joueur, self.quiz, 0)
        self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 2)

        historique = self.resultat_service.historique_joueur(self.joueur)
        self.assertEqual(len(historique), 2)
        self.assertTrue(all(r.id_utilisateur == self.joueur.id_utilisateur for r in historique))

    def test_statistiques_joueur(self):
        """Vérifie le calcul du nombre de passages, de la moyenne et du meilleur score."""
        self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 4)
        self.resultat_service.enregistrer_resultat(self.joueur, self.quiz, 2)

        stats = self.resultat_service.statistiques_joueur(self.joueur)
        self.assertEqual(stats["nb_passages"], 2)
        self.assertEqual(stats["moyenne"], 75.0)
        self.assertEqual(stats["meilleur"], 100.0)

    def test_statistiques_sans_historique(self):
        """Vérifie les statistiques d'un joueur n'ayant passé aucun quiz."""
        stats = self.resultat_service.statistiques_joueur(self.autre_joueur)
        self.assertEqual(stats, {"nb_passages": 0, "moyenne": 0.0, "meilleur": 0.0})


if __name__ == "__main__":
    unittest.main()
