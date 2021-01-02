from rest_framework import mixins, viewsets ,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Article
from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer

# Use RetrieveAPIView as the base class
class ArticleViewSet(
        viewsets.GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin
    ):

    # Set up permissions, renderers, and serializer
    # permission and renderer can take more than one class
    # The above should be written as tuple form
    # serializer take only one class
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    # Not sure what making
    queryset = Article.objects.select_related(
        'author', 'author__user'
    )
    lookup_field = 'slug'

    def create(self, request):

        article_context = {'author': request.user.article}
        article_data = request.data.get('article', {})

        serializer = self.serializer_class(data=article_data, context=article_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {}) 

        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        # We use the `select_related` method to avoid making unnecessary
        # database calls.
        # user__username 
        # -> user is field of article
        # -> username is field of user

        try:
            # select * from article
            # where article.slug = slug
            article = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(article)

        return Response(serializer.data, status=status.HTTP_200_OK) 