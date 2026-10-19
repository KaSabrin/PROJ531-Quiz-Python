
class User:
    def __init__(self, id, pseudo, email, mot_de_passe_hash, role="utilisateur"):
        self.id = id
        self.pseudo = pseudo
        self.email = email
        self.mot_de_passe_hash = mot_de_passe_hash
        self.role = role
