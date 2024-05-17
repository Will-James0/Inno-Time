from tkinter import *
from tkinter import ttk, messagebox
import time
import subprocess
import psycopg2

def update_pip(progress_bar):
    # Commande à exécuter
    commande = ["python", "-m", "pip", "install", "--upgrade", "pip"]

    # Exécuter la commande
    try:
        subprocess.check_call(commande)
        # messagebox.showinfo("Mise à jour de pip", "Mise à jour effectuée")
    except subprocess.CalledProcessError as e:
        messagebox.showwarning("",f"Erreur lors de la mise à jour de pip : {e}")

def install_module(progress_bar):
    # Liste des bibliothèques à installer
    libraries_to_install = ['pyzk','django','zklib','psycopg', 'psycopg2','pytz','pillow','python-dateutil']
    
    progress_bar["maximum"] = len(libraries_to_install)
    
    for i, library in enumerate(libraries_to_install, start=1):
        try:
            subprocess.run(['pip', 'install', library], check=True)
            
        except subprocess.CalledProcessError as e:
           messagebox.showwarning("",f"Erreur lors de l'installation de {library} : {e}")
    
        progress_bar["value"] = i
        progress_bar.update()
        time.sleep(1)
    # messagebox.showinfo("","library installée avec succès !.")
def create_database(progress_bar):
    try:
        # Connectez-vous à votre base de données PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Exécutez la requête SQL pour créer la base de données
        cursor.execute("CREATE DATABASE inno_time_bd OWNER postgres")

        # Fermez la connexion
        conn.close()
        # messagebox.showinfo("","La base de données a été créée avec succès.")
    except Exception as e:
        messagebox.showwarning("",f"Une erreur s'est produite lors de la création de la base de données : {e}")

def start_migration(progress_bar):
    try:
        subprocess.run(['python', '_internal\supertime\manage.py', 'migrate'], check=True)
        # messagebox.showinfo("","Migration réussie !.")
    except subprocess.CalledProcessError as e:
        messagebox.showwarning("",f"Erreur lors de la migration : : {e}")

def main():
    root = Tk()
    root.title("Configurations")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    window_width = 800
    window_height = 50
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Définir la taille et la position de la fenêtre
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    
    # Création de la barre de progression
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
    progress_bar.pack(pady=10,padx=15,)
    
    # Mise à jour de pip
    update_pip(progress_bar)
    
    # Installation des modules
    install_module(progress_bar)
    
    # Création de la base de données
    create_database(progress_bar)
    
    # Migration
    start_migration(progress_bar)
    
    root.destroy()
    # Fin de la configuration
    messagebox.showinfo("","FIN DE LA CONFIGURATION !.")
    
    root.mainloop()

if __name__ == "__main__":
    main()