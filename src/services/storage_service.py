"""Service de stockage : Gestion de la persistance des données au format JSON."""

import json
from pathlib import Path
from src.models.user import User
from src.models.quiz import Quiz
from src.models.resultat import Resultat


class StorageService:
    """Gère la lecture et l'écriture sécurisée des données dans des fichiers JSON."""

    def __init__(self, data_dir: str | Path | None = None):
        if data_dir is None:
            # Racine du projet : un cran au-dessus de 'src'
            project_root = Path(__file__).resolve().parent.parent.parent
            self.data_dir = project_root / "data"
        else:
            self.data_dir = Path(data_dir)

        # Création automatique du répertoire data s'il n'existe pas
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.users_file = self.data_dir / "users.json"
        self.quizzes_file = self.data_dir / "quizzes.json"
        self.results_file = self.data_dir / "results.json"

        self._init_files()

    def _init_files(self) -> None:
        """Initialise les fichiers JSON avec une liste vide s'ils n'existent pas encore."""
        for file_path in (self.users_file, self.quizzes_file, self.results_file):
            if not file_path.exists():
                self._write_json(file_path, [])

    def _read_json(self, file_path: Path) -> list[dict]:
        """Lit un fichier JSON et retourne une liste de dictionnaires."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_json(self, file_path: Path, data: list[dict]) -> bool:
        """Écrit des données structurées dans un fichier JSON avec encodage UTF-8."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except OSError as e:
            print(f"[Erreur stockage] Impossible d'écrire dans {file_path}: {e}")
            return False

    # --- Gestion des Utilisateurs ---
    def load_users(self) -> list[User]:
        """Charge l'ensemble des utilisateurs depuis users.json."""
        data = self._read_json(self.users_file)
        return [User.from_dict(item) for item in data]

    def save_users(self, users: list[User]) -> bool:
        """Enregistre la liste d'utilisateurs dans users.json."""
        data = [u.to_dict() for u in users]
        return self._write_json(self.users_file, data)

    # --- Gestion des Quiz (Sprint 3) ---
    def load_quizzes(self) -> list[Quiz]:
        """Charge l'ensemble des quiz depuis quizzes.json."""
        data = self._read_json(self.quizzes_file)
        return [Quiz.from_dict(item) for item in data]

    def save_quizzes(self, quizzes: list[Quiz]) -> bool:
        """Enregistre la liste de quiz dans quizzes.json."""
        data = [q.to_dict() for q in quizzes]
        return self._write_json(self.quizzes_file, data)

    # --- Gestion des Résultats (Sprint 4) ---
    def load_results(self) -> list[Resultat]:
        """Charge l'historique des résultats depuis results.json."""
        data = self._read_json(self.results_file)
        return [Resultat.from_dict(item) for item in data]

    def save_results(self, results: list[Resultat]) -> bool:
        """Enregistre la liste des résultats dans results.json."""
        data = [r.to_dict() for r in results]
        return self._write_json(self.results_file, data)
