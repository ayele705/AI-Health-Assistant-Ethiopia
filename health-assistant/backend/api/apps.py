from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """Start the reminder scheduler and preload translations when Django starts."""
        import os
        import logging
        logger = logging.getLogger(__name__)

        # Only run in the main process (not during migrate, test collection, etc.)
        if os.environ.get('RUN_MAIN') != 'true' and os.environ.get('DJANGO_SETTINGS_MODULE'):
            return

        # Start reminder scheduler
        try:
            from core.reminder_scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            logger.warning(f"Scheduler start failed: {e}")

        # Preload static translations into SQLite cache
        try:
            from django.conf import settings
            if getattr(settings, 'TRANSLATION_PRELOAD', True):
                translations_path = getattr(settings, 'TRANSLATIONS_JSON_PATH', None)
                if translations_path and translations_path.exists():
                    from core.translation_service import load_static_translations
                    count = load_static_translations(str(translations_path))
                    if count:
                        logger.info(f"Preloaded {count} translations from {translations_path}")
        except Exception as e:
            logger.warning(f"Translation preload failed: {e}")
