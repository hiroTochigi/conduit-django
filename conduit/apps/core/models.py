
from django.db import models

# Make abstract model -> this class does not make database
class TimestampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # abstract = True makes the class an abstract base model
    class Meta:
        abstract = True

        # - + field-name -> descending order
        # field-name -> ascending order
        # ? + field-name -> random order
        # This TimestampModel order data in a descending way (reverse chronologically)
        ordering = ['-created_at', '-updated_at']

    