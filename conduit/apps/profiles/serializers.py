"""
Serializer 
JSON object -> Python object
Then model can deal with the client request
Meta class define how model deal with the each data field
"""

# Need to have serializers to make custome serializers
from rest_framework import serializers

# Use model profile
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    # username -> user user.username
    username = serializers.CharField(source='user.username')
    # bio
    bio = serializers.CharField(allow_blank=True)

    # store image url 
    # serializers.SerializerMethodField() calls get_image method
    # because this serializers.SerializerMethodField() gives value to image variable
    image = serializers.CharField(allow_blank=True, required=False)
    following = serializers.SerializerMethodField()

    class Meta:
        # Use model profile
        model = Profile
        fields = ('username', 'bio', 'image', 'following',)

        # Not change user name at profile apps -> read only
        read_only_fields = ('username',)

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

    def get_following(self, instance): 
        """
        Check the user follow someone or not
        """

        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followee = instance

        return follower.is_following(followee)



        