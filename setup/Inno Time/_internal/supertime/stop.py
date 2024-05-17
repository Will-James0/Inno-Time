import os
import webbrowser

def runserver():
    try:
        # Demander à l'utilisateur de fournir le chemin du répertoire
        path = "_internal\supertime"
        # Vérifier si le chemin est valide
        if os.path.isdir(path):
            # Changer de répertoire
            os.chdir(path)

            # Exécuter la commande pour démarrer le serveur de développement Django
            os.system('stop.vbs')
        else:
            print("Le chemin du répertoire est invalide.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'exécution de la commande : {e}")

runserver()