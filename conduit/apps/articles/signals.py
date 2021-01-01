from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from conduit.apps.core.utils import generate_random_string

from .models import Article

# Register add_slug_to_article_if_not_exists function by using receiver decorator
# Before saving the article, check out the article has slug or not
# If not have slug, make slug
# slug is less than or equal 255 length
# end of the slug should have 6 unique character to prevent from having the
# exact same url
@receiver(post_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *ags, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:

        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) < MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH] 

        # combine slug and unique, then the new slug must be less than max length
        while len(f'{slug}-{unique}') < MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                # slug is only composed of just one part
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug + '-' + unique