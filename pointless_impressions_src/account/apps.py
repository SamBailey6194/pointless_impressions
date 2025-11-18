from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pointless_impressions_src.account'

    def ready(self):
        import pointless_impressions_src.account.signals
