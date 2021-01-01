from rest_framework import mixins, viewsets ,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Article
from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer

# Use RetrieveAPIView as the base class
class ArticleViewSet(
        viewsets.GenericViewSet,
        mixins.CreateModelMixin
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

    def create(self, request):

        article_context = {'author': request.user.profile}
        article_data = request.data.get('article', {})

        serializer = self.serializer_class(data=article_data, context=article_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)





