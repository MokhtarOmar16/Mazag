from core.models import User
from ..serializers.userprofile import UserProfileSerializer, SimpleUserProfileSerializer , UpdateUserProfileSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...pagination import CustomPagination

class ProfileViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.select_related('profile').all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleUserProfileSerializer
        return UserProfileSerializer



class MeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PATCH': return UpdateUserProfileSerializer 
        return UserProfileSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_object(self):
        return self.request.user
    

