from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Follow
from .userprofile import SimpleUserProfileSerializer

User = get_user_model()

class FollowersSerializer(serializers.ModelSerializer):
    follower = SimpleUserProfileSerializer()  

    class Meta:
        model = Follow
        fields = ['follower']

class FollowingSerializer(serializers.ModelSerializer):
    following = SimpleUserProfileSerializer()

    class Meta:
        model = Follow
        fields = ['following']
