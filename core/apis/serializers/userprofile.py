from rest_framework import serializers
from core.models import UserProfile, User




class BaseUserProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField() 
    
    def get_profile_picture(self, obj):
        # جلب الصورة من الملف الشخصي المتعلق بالمستخدم
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return obj.profile.profile_picture.url
        return None

    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = User
        fields = ["id","username", "first_name","profile_picture", 'is_following', "last_name" ]



class SimpleUserProfileSerializer(BaseUserProfileSerializer):

    class Meta(BaseUserProfileSerializer.Meta):
        pass


class UserProfileSerializer(BaseUserProfileSerializer):
    bio = serializers.ReadOnlyField(source="profile.bio")
    created_at = serializers.ReadOnlyField(source="profile.created_at")
    followers_count = serializers.IntegerField(read_only=1)
    following_count = serializers.IntegerField(read_only=1)
    class Meta(BaseUserProfileSerializer.Meta):        
        fields = BaseUserProfileSerializer.Meta.fields + ['bio', 'created_at', 'followers_count', 'following_count'] 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.resolver_match.view_name == 'profile-me': # delete is_following if its me action
            representation.pop('is_following', None)
        return representation
    