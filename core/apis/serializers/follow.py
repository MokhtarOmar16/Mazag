from rest_framework import serializers
from core.models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id','user','following_user',"created_at"]