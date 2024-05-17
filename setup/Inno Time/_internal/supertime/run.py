import os
import webbrowser
import django
import zk


def runserver():
    try:
        # Demander à l'utilisateur de fournir le chemin du répertoire
        path = "_internal\supertime"
        # Vérifier si le chemin est valide
        if os.path.isdir(path):
            # Changer de répertoire
            os.chdir(path)

            # Exécuter la commande pour démarrer le serveur de développement Django
            os.system('launch.vbs')

            # Ouvrir l'URL dans le navigateur par défaut
            webbrowser.open('http://localhost:8000/inno-time/')
        else:
            print("Le chemin du répertoire est invalide.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'exécution de la commande : {e}")

runserver()