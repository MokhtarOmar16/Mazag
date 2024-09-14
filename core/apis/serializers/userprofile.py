from rest_framework import serializers
from core.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')  
    username = serializers.ReadOnlyField(source='user.username')
    is_following = serializers.SerializerMethodField()
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    
    class Meta:
        model = UserProfile
        fields = ['user_id','first_name' ,"last_name",'id','bio', 'username', 'profile_picture', 'created_at', 'is_following', "followers_count", "following_count"]


    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            return user_profile.is_following(obj.id) 
        return False