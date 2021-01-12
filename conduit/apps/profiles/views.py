from rest_framework import status, serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView 

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer

# Use RetrieveAPIView as the base class
class ProfileRetrieveAPIView(RetrieveAPIView):

    # Set up permissions, renderers, and serializer
    # permission and renderer can take more than one class
    # The above should be written as tuple form
    # serializer take only one class
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    # I am not sure what is going on but it should have two table?
    queryset = Profile.objects.select_related('user')

    # Override retrieve method
    # Try to retrieve the requested profile and throw an exception if the
    # profile could not be found.
    def retrieve(self, request, username, *args, **kwargs):
        # We use the `select_related` method to avoid making unnecessary
        # database calls.
        # user__username 
        # -> user is field of profile
        # -> username is field of user

        try:
            # select * from profile
            # join user on profile.username = user.username
            # where user.username = username
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        serializer = self.serializer_class(
                profile, context={'request':request}
            )


        return Response(serializer.data, status=status.HTTP_200_OK) 

# View flow (RetrieveAPIView)
# Receive request
# 1. Retrieve data from database by the keyword from request (Client)
# 2. Check out whether the request can retrieve data or not
# 3. If data is not found -> RetrieveAPIView raise exception DoesNotExist
#    If found the data -> serialize the data (Python object)
# 4. Return the data with status, get request usually 200

class ProfileFollowAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer


    # delete use request and usernane
    def delete(self, request, username):
        
        # get user name profile -> follower
        follower = self.request.user.profile
        
        # Get profile object from user -> followee
        # doing error handling
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        # unfollow        
        follower.unfollow(followee)
        
        # make serializer class 
        serializer = self.serializer_class(
                followee, context={'request':request}
            )
        
        # return http response
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def post(self, request, username):

        # request -> the client who is authorized
        # the client follow a someone
        follower = self.request.user.profile
        
        try:
            # followee is specified in url
            # the followee name is store in username.
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username was not found")

        if follower.pk is followee.pk:
            raise serializers.ValidationError("You cannot follow yourself")

        follower.follow(followee)

        serializer = self.serializer_class(
            followee, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
