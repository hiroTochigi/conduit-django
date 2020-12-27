# Need to have serializers to make custome serializers
from rest_framework import serializers

# Use model profile
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    # username -> user User.username
    username = serializers.CharField(source=User.username)
    # bio
    bio = serializer.CharField(allow_blank=True)

    # store image url 
    # serializers.SerializerMethodField() calls get_image method
    # because this serializers.SerializerMethodField() gives value to image variable
    image = serializers.SerializerMethodField()

    class Meta:
        # Use model profile
        model = Profile
        fields = (username, bio, image,)

        # Not change user name at profile apps -> read only
        read_only_fields = (username,)

    # define get_image method
    # if image is found, user the image url
    # if not, use the default image url
    # https://static.productionready.io/images/smiley-cyrus.jpg'
    # obj should be request data from client 
    def get_image(self, obj):
        """
        If input has image url, use this url
        Otherwise use the default URL
        This method is called SerializerMethodField() to send value to image variable 
        """

        if obj.image:
            return obj.image
        return 'https://static.productionready.io/images/smiley-cyrus.jpg' 

    