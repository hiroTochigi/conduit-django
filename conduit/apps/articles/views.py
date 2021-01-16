from rest_framework import generics, mixins, viewsets ,status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment, Tag
from .renderers import ArticleJSONRenderer, CommentJSONRenderer
from .serializers import ArticleSerializer, CommentSerializer, TagSerializer

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

    def get_queryset(self):
        
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__username=author)
        
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        favorited = self.request.query_params.get('favorited', None)
        if favorited is not None:
            queryset = queryset.filter(favorited_by__user__username=favorited)

        return queryset

    def create(self, request):

        print(request.data)
        article_context = {
                'author': request.user.profile,
                'request': request
            }
        article_data = request.data.get('article', {})

        serializer = self.serializer_class(data=article_data, context=article_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        print(request.data)
        serializer_context = {'request':request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
                page,
                context=serializer_context,
                many=True
            )

        return self.get_paginated_response(serializer.data)

    def update(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {}) 
        serializer_context = {'request':request}

        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            context=serializer_context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        # We use the `select_related` method to avoid making unnecessary
        # database calls.
        # user__username 
        # -> user is field of article
        # -> username is field of user

        serializer_context = {'request':request}
        try:
            # select * from article
            # where article.slug = slug
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            )

        return Response(serializer.data, status=status.HTTP_200_OK) 
    

class CommentsListCreateAPIView(generics.ListCreateAPIView):

    # serializer take only one class
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer
    
    lookup_field = 'article__slug'
    # I am not sure why it is here
    # It is used to get article slug from kwarg
    # Client sends the slug, and urls.py pass the slug
    # as dictionary whose key is article_slug
    lookup_url_kwarg = 'article_slug'
    # I have no idea what is doing
    # Get all comment object from DB 
    # before Django starts being to about to receive http request
    # from Client  
    queryset = Comment.objects.select_related(
        'article', 'article__author', 'article__author__user',
        'author', 'author__user'
    )

    # I have no idea what going on
    # Only what I know here is make query whose key is article__slug and 
    # the value is came from client whose dictionary whose key is article_slug  
    # What inside is the dictionary
    def filter_queryset(self, queryset):
        # The built-in list function calls `filter_queryset`. Since we only
        # want comments for a specific article, this is a good place to do
        # that filtering.
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        # Filter and return all comments whose slug which the Client request
        return queryset.filter(**filters)

    def create(self, request, article_slug=None):

        data = request.data.get('comment', {})
        context = {'author': request.user.profile}

        # get article from Article database whose slug is came from the client
        # Why article_slug value contains the slug from the client?  
        try:
            # create receives the slug which the client requests 
            # inside the variable article_slug
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        # data has the comment from client
        # context has the comment author and the article
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentsDestroyAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'comment_pk'
    queryset = Comment.objects.all()

    def delete(self, request, article_slug=None, comment_pk=None):

        try: 
            comment = self.queryset.get(id=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ArticleFavoriteAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def delete(self, request, article_slug=None):

        profile = request.user.profile
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        profile.unfavorite(article)
        serializer = self.serializer_class(
            article,
            context=serializer_context,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_slug=None):

        profile = request.user.profile
        serializer_context = {'request': request}
        
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        profile.favorite(article)
        serializer = self.serializer_class(
            article,
            context=serializer_context,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagListAPIView(generics.ListAPIView):

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(
            serializer_data,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        return Article.objects.filter(
            author__in=self.request.user.profile.follows.all()
        )
    
    def list(self, request):
        queryset = self.get_queryset()
        page = paginate_queryset(queryset)
        serializer_context = {'request':request}
        serializer = serializer_class(page, serializer_class, many=True)
        return get_paginated_response(serializer.data) 

    
