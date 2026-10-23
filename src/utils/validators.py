"""Module de validation des entrées utilisateur."""

import re

EMAIL_REGEX = re.compile(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$")


def validate_email(email: str) -> bool:
    """Vérifie si une adresse e-mail est dans un format valide."""
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_pseudo(pseudo: str) -> tuple[bool, str]:
    """Valide le format d'un pseudonyme.

    Règles :
    - Entre 3 et 30 caractères.
    - Caractères alphanumériques, tirets et underscores uniquement.
    """
    if not isinstance(pseudo, str):
        return False, "Le pseudo doit être une chaîne de caractères."

    cleaned = pseudo.strip()
    if len(cleaned) < 3:
        return False, "Le pseudo doit contenir au moins 3 caractères."
    if len(cleaned) > 30:
        return False, "Le pseudo ne peut pas dépasser 30 caractères."
    if not re.match(r"^[\w-]+$", cleaned):
        return False, "Le pseudo ne doit contenir que des lettres, chiffres, tirets et underscores."

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Valide la complexité minimale d'un mot de passe.

    Règles :
    - Minimum 6 caractères.
    - Au moins une lettre et au moins un chiffre.
    """
    if not isinstance(password, str):
        return False, "Le mot de passe doit être une chaîne de caractères."

    if len(password) < 6:
        return False, "Le mot de passe doit comporter au moins 6 caractères."
    if not any(c.isalpha() for c in password):
        return False, "Le mot de passe doit contenir au moins une lettre."
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre."

    return True, ""
