from django.apps import AppConfig


class CommunityHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community_hub'
    
    def ready(self):
        import community_hub.signals
