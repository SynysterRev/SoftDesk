from rest_framework import viewsets

from users.permissions import SelfResourceAccess
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | SelfResourceAccess]
