from django.apps import AppConfig


class ReferendamainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'referendaMain'

    def ready(self):
        import referendaMain.signals
