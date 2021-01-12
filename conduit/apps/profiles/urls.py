from django.urls import path

from .views import (
    ProfileRetrieveAPIView,
    ProfileFollowAPIView,
)

app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>', ProfileRetrieveAPIView.as_view()),
    path('profiles/<str:username>/profile', ProfileFollowAPIView.as_view()),
]