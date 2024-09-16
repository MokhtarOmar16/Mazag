from core.models import User
from ..serializers.userprofile import UserProfileSerializer, SimpleUserProfileSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count

class ProfileViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.select_related('profile')\
        .annotate(followers_count=Count('user_followers'),
                  following_count=Count('user_following'))\
        .all()
    
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
        user = User.objects.annotate(
            followers_count=Count('user_followers'),
            following_count=Count('user_following')
        ).get(id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = self.get_serializer(user, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
