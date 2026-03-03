"""
App Configuration for Core Module
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Academic Admission System'
    
    def ready(self):
        """Import signals when app is ready"""
        import core.signals  # noqa

