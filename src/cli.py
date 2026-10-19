
def menu_principal():
    while True:
        print("\n===== BIENVENUE SUR QUIZORA =====")
        print("1. Créer un compte")
        print("2. Se connecter")
        print("3. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            print("Inscription : fonctionnalité en cours de développement.")

        elif choix == "2":
            print("Connexion : fonctionnalité en cours de développement.")

        elif choix == "3":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")
