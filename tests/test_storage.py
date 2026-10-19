"""Tests unitaires du service de stockage JSON."""

import tempfile
import unittest
from pathlib import Path
from src.models.user import User
from src.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):
    def setUp(self):
        """Initialise un dossier temporaire pour isoler les tests."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageService(data_dir=self.temp_dir.name)

    def tearDown(self):
        """Nettoie le dossier temporaire après chaque test."""
        self.temp_dir.cleanup()

    def test_initial_files_created(self):
        """Vérifie que les fichiers JSON nécessaires sont créés automatiquement."""
        users_file = Path(self.temp_dir.name) / "users.json"
        quizzes_file = Path(self.temp_dir.name) / "quizzes.json"
        results_file = Path(self.temp_dir.name) / "results.json"

        self.assertTrue(users_file.exists())
        self.assertTrue(quizzes_file.exists())
        self.assertTrue(results_file.exists())

    def test_save_and_load_users(self):
        """Vérifie la sérialisation et la désérialisation d'utilisateurs."""
        user = User(
            pseudo="alice",
            email="alice@example.com",
            mdp_hash="dummy_hash",
            role=User.ROLE_JOUEUR,
        )
        self.storage.save_users([user])

        loaded_users = self.storage.load_users()
        self.assertEqual(len(loaded_users), 1)
        self.assertEqual(loaded_users[0].pseudo, "alice")
        self.assertEqual(loaded_users[0].email, "alice@example.com")
        self.assertEqual(loaded_users[0].role, User.ROLE_JOUEUR)


if __name__ == "__main__":
    unittest.main()
