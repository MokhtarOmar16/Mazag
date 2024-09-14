from core.models import UserProfile
from ..serializers.userprofile import UserProfileSerializer, SimpleUserProfileSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class UserProfileViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin, GenericViewSet):
    queryset= UserProfile.objects.select_related('user').all()
    
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleUserProfileSerializer 
        return UserProfileSerializer  
    
    
    def get_serializer_context(self):
        return {"request":self.request}

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = UserProfile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer =UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        profile = self.get_object()
        profile.follow(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        profile = self.get_object()
        profile.unfollow(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        return Response()