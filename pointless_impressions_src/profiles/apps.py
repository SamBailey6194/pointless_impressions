from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pointless_impressions_src.profiles'

    # def ready(self):
    #     import pointless_impressions_src.profiles.signals
