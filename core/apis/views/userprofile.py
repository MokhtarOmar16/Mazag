from core.models import UserProfile
from ..serializers.userprofile import UserProfileSerializer, SimpleUserProfileSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
class ProfileViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('user__followers', 'user__following').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleUserProfileSerializer
        return UserProfileSerializer
    
    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
