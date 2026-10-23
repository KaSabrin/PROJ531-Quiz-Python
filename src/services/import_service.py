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
                    
                    if "[" in enonce_brut and "pts]" in enonce_brut:
                        parties = enonce_brut.split("[")
                        enonce = parties[0].strip()
                        pts_str = parties[1].replace("pts]", "").replace("pt]", "").strip()
                        try:
                            points = int(pts_str)
                        except ValueError:
                            points = 1
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
        print(f"❌ Erreur : Le fichier {chemin_fichier} est introuvable.")
        return None

    return quiz

if __name__ == "__main__":
    # Test rapide de la fonction
    # Assure-toi d'avoir un fichier test.txt dans ton dossier ou indique un chemin valide
    import json
    resultat = importer_quiz_depuis_txt("test.txt")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
    
