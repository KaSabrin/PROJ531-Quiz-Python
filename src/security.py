"""Module de sécurité : hachage et vérification des mots de passe.

Format de stockage (champ ``mdp_hash`` de data/users.json) :
    "<sel>$<empreinte>"
où le sel est une chaîne hexadécimale aléatoire (16 octets) et l'empreinte
le SHA-256 de ``sel + mot_de_passe``, en hexadécimal.
"""

import hashlib
import hmac
import secrets

SALT_BYTES = 16          # 16 octets -> 32 caractères hexadécimaux
SEPARATOR = "$"


def _digest(salt: str, password: str) -> str:
    """Calcule l'empreinte SHA-256 de ``sel + mot de passe`` (UTF-8)."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """Hache un mot de passe avec un sel aléatoire.

    Retourne une chaîne ``"sel$empreinte"`` prête à être stockée.
    Lève ``TypeError`` si le mot de passe n'est pas une chaîne et
    ``ValueError`` s'il est vide.
    """
    if not isinstance(password, str):
        raise TypeError("Le mot de passe doit être une chaîne de caractères.")
    if password == "":
        raise ValueError("Le mot de passe ne peut pas être vide.")
    salt = secrets.token_hex(SALT_BYTES)
    return f"{salt}{SEPARATOR}{_digest(salt, password)}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Vérifie un mot de passe par rapport à un ``"sel$empreinte"`` stocké.

    La comparaison se fait en temps constant (``hmac.compare_digest``) pour
    éviter les attaques par mesure de temps. Retourne ``False`` (sans lever
    d'exception) si une des entrées est invalide ou mal formée.
    """
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        return False
    salt, sep, expected = stored_hash.partition(SEPARATOR)
    if not sep or not salt or not expected:
        return False
    return hmac.compare_digest(_digest(salt, password), expected)

