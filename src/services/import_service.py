import re

# Barème en fin d'énoncé : "[1 pt]" ou "[2 pts]"
BAREME_REGEX = re.compile(r"\[\s*(\d+)\s*pts?\s*\]\s*$", re.IGNORECASE)


def importer_quiz_depuis_txt(chemin_fichier):
    """
    Lit un fichier texte structuré pour importer un quiz.
    Format attendu :
    TITRE: ...
    DESCRIPTION: ...
    QUESTION: ... [X pts]
    - Réponse fausse
    * Réponse correcte
    """
    quiz = {"titre": "", "description": "", "questions": []}
    current_question = None

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue

                if ligne.startswith("TITRE:"):
                    quiz["titre"] = ligne.replace("TITRE:", "").strip()
                elif ligne.startswith("DESCRIPTION:"):
                    quiz["description"] = ligne.replace("DESCRIPTION:", "").strip()
                elif ligne.startswith("QUESTION:"):
                    if current_question:
                        quiz["questions"].append(current_question)

                    enonce_brut = ligne.replace("QUESTION:", "").strip()
                    points = 1
                    bareme = BAREME_REGEX.search(enonce_brut)
                    if bareme:
                        points = int(bareme.group(1))
                        enonce = enonce_brut[:bareme.start()].strip()
                    else:
                        enonce = enonce_brut

                    current_question = {"enonce": enonce, "points": points, "options": []}
                elif ligne.startswith("-") or ligne.startswith("*"):
                    if current_question is not None:
                        est_correcte = ligne.startswith("*")
                        texte_option = ligne[1:].strip()
                        current_question["options"].append({"texte": texte_option, "est_correcte": est_correcte})

            if current_question:
                quiz["questions"].append(current_question)

    except FileNotFoundError:
        print(f"Erreur : Le fichier {chemin_fichier} est introuvable.")
        return None

    return quiz


if __name__ == "__main__":
    # Test rapide de la fonction
    import json
    resultat = importer_quiz_depuis_txt("sample_quiz.txt")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
