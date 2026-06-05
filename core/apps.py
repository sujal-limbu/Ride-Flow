from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.core.management import call_command
        call_command('release_vehicles')  
        from . import scheduler
        scheduler.start()  