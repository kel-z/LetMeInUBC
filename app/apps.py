from django.apps import AppConfig
from . import app_main
import os


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            app_main.start_scheduler()
