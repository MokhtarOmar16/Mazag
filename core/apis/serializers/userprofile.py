from rest_framework import serializers
from core.models import UserProfile




class BaseUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')  
    username = serializers.ReadOnlyField(source='user.username')
    is_following = serializers.SerializerMethodField()
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    

    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = UserProfile
        fields = ["id","username", "first_name","profile_picture", 'is_following', "last_name" ]



class SimpleUserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')  # جلب user.id من العلاقة
    username = serializers.ReadOnlyField(source='user.username')  # جلب user.username
    first_name = serializers.ReadOnlyField(source='user.first_name')  # جلب user.first_name
    last_name = serializers.ReadOnlyField(source='user.last_name')  # جلب user.last_name

    class Meta:
        model = UserProfile
        fields = ['user_id', 'username', 'first_name', 'last_name', 'profile_picture', 'bio']




class UserProfileSerializer(BaseUserProfileSerializer):
    class Meta(BaseUserProfileSerializer.Meta):        
        fields = BaseUserProfileSerializer.Meta.fields + ['bio', 'created_at', 'is_following', "followers_count", "following_count"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.resolver_match.view_name == 'profile-me':
            representation.pop('is_following', None)
        return representation
    