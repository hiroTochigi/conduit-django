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
from .models import Article, Comment, Tag
from .relations import TagRelatedField

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
    
    favorited = serializers.SerializerMethodField()
    favoritedCount = serializers.SerializerMethodField(
        method_name='get_favorited_count'
    )

    tagList = TagRelatedField(many=True, required=False, source='tags')
    print("tagList")
    print(tagList)

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
            'favorited',
            'favoritedCount',
            'tagList',
            'author',
            'createdAt',
            'updatedAt',
        )

    # override create to retrieve author from context
    # What is the context of serializers.ModelSerializer?
    def create(self, validated_data):

        print("validated_data")
        print(validated_data)
        # Where context fame from?
        author = self.context.get('author', None)

        # Why have to use pop instead get
        tags = self.validated_data.pop('tags', [])
        # tags = self.validated_data.get('tags', [])
        article = Article.objects.create(author=author, **validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article 

    # Why created_at? the variable came from client like this?
    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        # check out the client already favorite an article or not
        return request.user.profile.has_favorited(instance)
    
    # Check out how many favorite has the article
    # It look at the instance favorited_by table 
    # (It is the intermiddle table connect to profile and article 
    # ManyToMany relationship) 
    def get_favorited_count(self, instance):
        return instance.favorited_by.count()
    
class CommentSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    body = serializers.CharField() 

    # Why this is not needed?
    #article = ArticleSerializer(read_only=True)

    # Call get_[~~~]_at 
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment 
        # Why id is here and article is not in the fields?
        fields = (
            'id',
            'body',
            'author',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):

        # Where context fame from?
        author = self.context.get('author', None)
        article = self.context.get('article', None)

        return Comment.objects.create(author=author, article=article, **validated_data)
    
    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, obj):
        return obj.tag

    

        