
from django.db import models
# Add absolute path from top directory of Django project
from conduit.apps.core.models import TimestampedModel

class Profile(TimestampedModel):

    # UserProfile has user basic infomation such as
    # username, email, password
    # Only authenticated user is allowed to have only one user profile
    # If the authenticated user is deleted, this profile also is deleted
    # automatically. 
    # This deletion is realized by on_delete=models.CASCADE
    user = models.OneToOneField(
        'authentication.User', 
        on_delete=models.CASCADE
    )

    # User have biography and avatar
    # Both of field are not mandatory
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)


    def __str__(self):

        return self.user.username