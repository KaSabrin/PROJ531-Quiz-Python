"""Tests unitaires du module de sécurité."""

import unittest
from src.security import hash_password, verify_password


class TestSecurity(unittest.TestCase):
    def test_hash_format(self):
        """Vérifie que le mot de passe est bien haché au format salt$hash."""
        pwd = "MonMotDePasse123"
        hashed = hash_password(pwd)
        self.assertIn("$", hashed)
        salt, hash_val = hashed.split("$")
        self.assertEqual(len(salt), 32)  
        self.assertEqual(len(hash_val), 64)  

    def test_verify_password_success(self):
        """Vérifie qu'un mot de passe correct est validé."""
        pwd = "SecretPassword42"
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(pwd, hashed))

    def test_verify_password_failure(self):
        """Vérifie qu'un mauvais mot de passe est rejeté."""
        pwd = "SecretPassword42"
        hashed = hash_password(pwd)
        self.assertFalse(verify_password("MauvaisMotDePasse", hashed))

    def test_salting_uniqueness(self):
        """Vérifie que deux hachages du même mot de passe produisent des hash différents (grâce au sel)."""
        pwd = "Identique123"
        hash1 = hash_password(pwd)
        hash2 = hash_password(pwd)
        self.assertNotEqual(hash1, hash2)


if __name__ == "__main__":
    unittest.main()
