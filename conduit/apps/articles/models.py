
from django.db import models
# Add absolute path from top directory of Django project
from conduit.apps.core.models import TimestampedModel

class Article(TimestampedModel):

    # slug is newspaper term
    # slug is short label using URL
    # db_index = True -> db makes index for the field 
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    title = models.CharField(max_length=255, db_index=True)

    description = models.TextField()
    body = models.TextField()

    # Every article must have an author. This will answer questions like "Who
    # gets credit for writing this article?" and "Who can edit this article?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `Article`s.
    
    # To refer to models defined in another application, 
    # you can explicitly specify a model with the full application label. 

    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles'
    ) 

    def __str__(self):
        return self.title 
