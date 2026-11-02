import sys

# PROJ531 : Application de quiz "Quizora"
from src.cli import lancer


def main():
    """Point d'entrée principal. Lance l'interface graphique avec --gui, sinon la console."""
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--gui", "-g", "gui"):
        from src.gui import lancer_gui  # import différé : Tkinter n'est requis que pour la GUI
        lancer_gui()
    else:
        lancer()


if __name__ == "__main__":
    main()
