
from django.apps import AppConfig

class ArticleAppConfig(AppConfig):
    name = 'conduit.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import conduit.apps.articles.signals

# inform Django to use this overridden Application
# Django official manual does not recommend this way to inform Django to use this app
# Instead of the way, explicitly include the application in INSTALLED_APPS
default_app_config = 'conduit.apps.articles.ArticleAppConfig'