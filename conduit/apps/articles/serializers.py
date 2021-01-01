"""
Serializer 
JSON object -> Python object
Then model can deal with the client request
Meta class define how model deal with the each data field
"""

# Need to have serializers to make custome serializers
from rest_framework import serializers

from conduit.apps.profiles.serializers import ProfileSerializer
# Use model profile
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):

    # Three variables are specified here because they are not used
    # directly from Article model

    # This is my guess, but
    # author came from profiles.Profile model
    # Therefore, assigned ProfileSerializer with read_only=True

    # author field is defined in models.py like below
    # author = models.ForeignKey(
    #    'profiles.Profile', on_delete=models.CASCADE, related_name='articles')

    author = ProfileSerializer(read_only=True)

    # There are no TextField in serializer
    # Therefore use CharField with required=False
    description = serializers.CharField(required=False) 
    body = serializers.CharField(required=False) 

    # Call get_[~~~]_at 
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        # Use model profile
        model = Article
        fields = (
            'slug',
            'title',
            'description',
            'body',
            'author',
            'createdAt',
            'updatedAt',
        )

    # override create to retrieve author from context
    # What is the context of serializers.ModelSerializer?
    def create(self, validated_data):

        # Where context fame from?
        author = self.context.get('author', None)

        return Article.objects.create(author=author, **validated_data)

    # Why created_at? the variable came from client like this?
    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    