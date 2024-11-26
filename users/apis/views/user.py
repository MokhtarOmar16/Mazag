from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user import UserSerializer, MeSerializer, ChangePasswordSerializer
from ..views.base_viewsets import RetrieveUpdateDestroyViewSet



class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer




class UserMeViewSet(RetrieveUpdateDestroyViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        return MeSerializer



class ChangePasswordView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)