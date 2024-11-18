from rest_framework import serializers
from core.models import UserProfile, User
from django.core.cache import cache
from django.db.models import Count



class BaseUserProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField() 
    
    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return obj.profile.profile_picture.url
        return None

    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.user_followers.filter(id=request.user.id).exists()
        return False
    
    def get_cached_count(self, obj, cache_key_prefix, related_field, timeout=300):
        cache_key = f"{cache_key_prefix}_{obj.id}"
        count = cache.get(cache_key)

        if count is None:
            # If not in cache, fetch from the database and store in cache
            count = getattr(obj, related_field).count()
            cache.set(cache_key, count, timeout=timeout)

        return count

    class Meta:
        model = User
        fields = ["id","username", "first_name","profile_picture", 'is_following', "last_name" ]



class SimpleUserProfileSerializer(BaseUserProfileSerializer):

    class Meta(BaseUserProfileSerializer.Meta):
        pass


class UserProfileSerializer(BaseUserProfileSerializer):
    bio = serializers.ReadOnlyField(source="profile.bio")
    created_at = serializers.ReadOnlyField(source="profile.created_at")
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return self.get_cached_count(obj, "user_followers_count", "user_followers")

    def get_following_count(self, obj):
        return self.get_cached_count(obj, "user_following_count", "user_following")
    

    class Meta(BaseUserProfileSerializer.Meta):        
        fields = BaseUserProfileSerializer.Meta.fields + ['bio', 'created_at', 'followers_count', 'following_count'] 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.resolver_match.view_name == 'profile-me': # delete is_following if its me action
            representation.pop('is_following', None)
        return representation


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False) 
    last_name = serializers.CharField(required=False)  
    bio = serializers.CharField(source='profile.bio', required=False,allow_blank=True)  
    profile_picture = serializers.ImageField(source='profile.profile_picture', required=False, allow_null=True)  

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']

    def update(self, instance, validated_data):
        
        # Update User model fields (first_name, last_name)
        if 'first_name' in validated_data:
            instance.first_name = validated_data.get('first_name', instance.first_name)
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update UserProfile model fields (bio, profile_picture)
        profile_data = validated_data.get('profile', {})
        profile = instance.profile

        profile.bio = profile_data.get('bio', profile.bio)
        if 'profile_picture' in profile_data:
            profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.save()

        return instance

