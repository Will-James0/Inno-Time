from django.apps import AppConfig


class ProfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profil'

    def ready(self):
        from . import scheduler
        scheduler.start()

    
