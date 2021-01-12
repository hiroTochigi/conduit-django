
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

    """
    Make many to many field
    Django makes an intermediate table for the many-to-many relationship
    self is itself -> my profile instance
    related_name defines the name of manager -> followed_by
    you can query this intermediate table via followed_by
    symmetrical=False -> the relationship is not symmetrical
    you are followed by someone does not mean you follow this someone
    """
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    """
    Why there is no symmetrical=False
    """
    favorites = models.ManyToManyField(
        'articles.Article',
        related_name='favorited_by',
    )

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """add profile -> the client follow the profile"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """remove profile -> the client unfollow the someone"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """check out the client is following someone"""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed(self, profile):
        """
        check out the client is followed by someone
        """
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article):
        """add follower -> the client follow the someone"""
        self.favorites.add(article)

    def unfavorite(self, article):
        """remove follower -> the client unfollow the someone"""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Returns True if we have favorited `article`; else False."""
        print(article)
        print(dir(article))
        print(article.pk)
        return self.favorites.filter(pk=article.pk).exists()
