from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
   ArticleViewSet,
   ArticleFavoriteAPIView,
   ArticleFeedAPIView,
   CommentsListCreateAPIView,
   CommentsDestroyAPIView,
   TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

app_name = 'articles'
urlpatterns = [
    path(
        'articles/feed',
        ArticleFeedAPIView.as_view()
    ),
    path(
            # slug (<- variable type):article_slug(<- variable name)
            'articles/<slug:article_slug>/comments',
            CommentsListCreateAPIView.as_view()
        ),
    path(
            # slug (<- variable type):article_slug(<- variable name)
            'articles/<slug:article_slug>/favorite',
            ArticleFavoriteAPIView.as_view()
        ),
    path(
            'articles/<slug:article_slug>/comments/<int:comment_pk>',
            CommentsDestroyAPIView.as_view()
        ),
    path('tags', TagListAPIView.as_view()),
    path('', include(router.urls)),
]