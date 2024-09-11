from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core import models as CoreModels
# from ..serializers.follow import UserFollowingSerializer


class UserFollowingViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    # serializer_class = UserFollowingSerializer
    queryset = CoreModels.Follow.objects.all()
