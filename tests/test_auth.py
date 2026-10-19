"""Tests unitaires du service d'authentification."""

import tempfile
import unittest
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.storage_service import StorageService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        """Initialise un stockage et un service d'authentification isolés."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageService(data_dir=self.temp_dir.name)
        # On vide la liste par défaut créée pour tester l'inscription from scratch
        self.storage.save_users([])
        self.auth = AuthService(storage_service=self.storage)
        self.storage.save_users([])  # remise à zéro

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_success(self):
        """Vérifie une inscription valide."""
        success, msg, user = self.auth.register("martin", "martin@test.fr", "MotDePasse1")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.pseudo, "martin")
        self.assertEqual(user.email, "martin@test.fr")
        self.assertEqual(user.role, User.ROLE_JOUEUR)

    def test_register_duplicate_pseudo(self):
        """Vérifie le rejet d'un doublon de pseudo."""
        self.auth.register("dupont", "dupont1@test.fr", "MotDePasse1")
        success, msg, _ = self.auth.register("dupont", "dupont2@test.fr", "MotDePasse2")
        self.assertFalse(success)
        self.assertIn("déjà utilisé", msg)

    def test_register_duplicate_email(self):
        """Vérifie le rejet d'un doublon d'email."""
        self.auth.register("userA", "commun@test.fr", "MotDePasse1")
        success, msg, _ = self.auth.register("userB", "commun@test.fr", "MotDePasse2")
        self.assertFalse(success)
        self.assertIn("déjà enregistrée", msg)

    def test_register_invalid_email(self):
        """Vérifie le rejet d'une adresse email invalide."""
        success, msg, _ = self.auth.register("bob", "adresse_invalide", "MotDePasse1")
        self.assertFalse(success)
        self.assertIn("invalide", msg)

    def test_register_weak_password(self):
        """Vérifie le rejet d'un mot de passe trop court ou sans chiffre."""
        success, msg, _ = self.auth.register("bob", "bob@test.fr", "court")
        self.assertFalse(success)

    def test_login_success_with_pseudo(self):
        """Vérifie la connexion réussie avec le pseudo."""
        self.auth.register("claire", "claire@test.fr", "MotDePasse1")
        success, msg, user = self.auth.login("claire", "MotDePasse1")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(self.auth.get_current_user().pseudo, "claire")

    def test_login_success_with_email(self):
        """Vérifie la connexion réussie avec l'e-mail."""
        self.auth.register("claire", "claire@test.fr", "MotDePasse1")
        success, msg, user = self.auth.login("claire@test.fr", "MotDePasse1")
        self.assertTrue(success)
        self.assertIsNotNone(user)

    def test_login_wrong_password(self):
        """Vérifie le rejet de connexion en cas de mauvais mot de passe."""
        self.auth.register("claire", "claire@test.fr", "MotDePasse1")
        success, msg, user = self.auth.login("claire", "MauvaisMdp99")
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertFalse(self.auth.is_authenticated())

    def test_logout(self):
        """Vérifie la déconnexion."""
        self.auth.register("claire", "claire@test.fr", "MotDePasse1")
        self.auth.login("claire", "MotDePasse1")
        self.assertTrue(self.auth.is_authenticated())
        self.auth.logout()
        self.assertFalse(self.auth.is_authenticated())


if __name__ == "__main__":
    unittest.main()
