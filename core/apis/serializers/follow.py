from rest_framework import serializers
from core.models import Follow
from .userprofile import SimpleUserProfileSerializer

class FollowersSerializer(serializers.ModelSerializer):
    follower = SimpleUserProfileSerializer()
    class Meta:
        model = Follow
        fields = ['follower']


class FollowingSerializer(serializers.ModelSerializer):
    following = SimpleUserProfileSerializer(many=1)

    class Meta:
        model = Follow
        fields = ['following']