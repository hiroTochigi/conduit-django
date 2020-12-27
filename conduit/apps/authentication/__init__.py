
from django.apps import AppConfig

class AuthenticationAppConfig(AppConfig):

    # name, label attributes must be defined in order to make 
    # subcalass from AppConfig?

    # Full Python Path to the application
    # It must be unique on entire Django project
    name = 'conduit.apps.authentication'

    # Short name of theapplication
    # It must be unique on entire Django project
    label = 'authentication'

    # Human-readable name of the appliication
    verbose_name = 'Authentication'

    # ready method initialize this application
    # override ready method to register signals on the authentication app
    def ready(self):
        import conduit.apps.authentication.signals

# inform Django to use this overridden Application
# Django official manual does not recommend this way to inform Django to use this app
# Instead of the way, explicitly include the application in INSTALLED_APPS
default_app_config = 'conduit.apps.authentication.AuthenticationAppConfig'