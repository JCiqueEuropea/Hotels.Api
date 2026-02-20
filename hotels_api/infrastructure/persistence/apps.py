from django.apps import AppConfig


class PersistenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotels_api.infrastructure.persistence'
    verbose_name = 'Hotels Persistence'

    def ready(self):
        # Importar modelos para que Django los registre aunque estén en un subpaquete
        from . import models  # noqa: F401
