from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User
from conduit.apps.profiles.serializers import ProfileSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )


        if password is None:
            raise serializers.ValidationError(
                'An password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        return {
            "email": user.email,
            "username": user.username,
            "user": user.token,
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128 
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.

    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        read_only = True
    )

    # When a field should be handled as a serializer, we must explicitly say
    # so. Moreover, `UserSerializer` should never expose profile information,
    # so we set `write_only=True`.
    profile = ProfileSerializer(write_only=True)

    # We want to get the `bio` and `image` fields from the related Profile
    # model.
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = (
            "email", "username", "password", "token",
            "profile", "bio", "image", 
        )

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and 
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ("token",)

    def update(self, instance, validated_data):

        # password should be deleted from validated_data
        # without deleting password, password is stored as 
        # usual variable
        password = validated_data.pop("password", None)
        
        # profile is separated table, so we do not want to
        # include profile data when updating user table
        profile_data = validated_data.pop("profile", {})

        for key, value in validated_data.items():

            setattr(instance, key, value)

        # password should be hashed nd salted
        # set_password method takes care of it
        if password is not None:
            instance.set_password(password)

        # Update User model(table)
        instance.save()

        # Update profile model(table)
        for key, value in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()

        return instance