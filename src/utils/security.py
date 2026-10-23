"""Module de sécurité : Hachage cryptographique et vérification des mots de passe.

Ce module implémente les bonnes pratiques de sécurité OWASP :
- Ne jamais stocker de mots de passe en clair.
- Utilisation d'un algorithme de hachage robuste (SHA-256).
- Utilisation d'un sel cryptographique unique par utilisateur (secrets.token_hex)
  pour contrer les attaques par dictionnaire et tables arc-en-ciel.
- Comparaison à temps constant (hmac.compare_digest) pour contrer les attaques par canal auxiliaire (timing attacks).
"""

import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    """Hache un mot de passe avec un sel aléatoire généré cryptographiquement.

    Args:
        password: Le mot de passe en clair.

    Returns:
        Une chaîne au format 'salt$hash_hex'.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Le mot de passe doit être une chaîne non vide.")

    # Génération d'un sel aléatoire de 16 octets (32 caractères hex)
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256()
    hash_obj.update(salt.encode("utf-8"))
    hash_obj.update(password.encode("utf-8"))
    password_hash = hash_obj.hexdigest()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Vérifie si un mot de passe en clair correspond au condensat stocké.

    Args:
        password: Le mot de passe en clair fourni par l'utilisateur.
        stored_hash: Le hachage stocké sous la forme 'salt$hash_hex'.

    Returns:
        True si le mot de passe est valide, False sinon.
    """
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        return False

    parts = stored_hash.split("$")
    if len(parts) != 2:
        return False

    salt, original_hash = parts

    hash_obj = hashlib.sha256()
    hash_obj.update(salt.encode("utf-8"))
    hash_obj.update(password.encode("utf-8"))
    computed_hash = hash_obj.hexdigest()

    # Comparaison à temps constant pour éviter les attaques temporelles
    return hmac.compare_digest(original_hash, computed_hash)
