from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # This must match the folder path in your project
    name = 'apps.payments'