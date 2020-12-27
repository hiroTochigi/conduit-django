from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    # Override retrieve method
    # Try to retrieve the requested profile and throw an exception if the
    # profile could not be found.
    def retrieve(self, request):
        # We use the `select_related` method to avoid making unnecessary
        # database calls.
        # user__username 
        # -> user is field of profile
        # -> username is field of user

        try:
            profile = Profile.objects.selected_related('user').get(
                user__username=request.user
                )
        except Profile.DoesNotExist:
            raise

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK) 


# View flow (RetrieveAPIView)
# Recieve request
# Retrieve data from database by the keyword from request (Client)
# Check out whether the request can retrieve data or not
# If data is not found -> RetrieveAPIView raise exception DoesNotExist
# If found the data -> serialize the data (Python object)
# Return the data with status, get request usually 200




