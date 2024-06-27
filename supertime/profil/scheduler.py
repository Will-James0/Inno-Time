# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# def get_log_all():
#     url = 'http://localhost:8000/inno-time/dowloands/log-alls/'  # Remplacez par l'URL correcte
#     response = requests.get(url)
#     if response.status_code == 200:
#         print('Requête réussie')
#     else:
#         print('Erreur de requête//////////////////////', response.status_code)

def get_log():
    url = 'http://localhost:8000/inno-time/dowloands/attendance/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Oui c'est toi")
    else:
        print('Erreur de requête', response.status_code)

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(get_log_all, 'interval', seconds=15)
    scheduler.add_job(get_log, 'interval', seconds=15)
    scheduler.start()
