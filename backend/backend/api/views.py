from django.contrib.auth.models import User
from rest_framework import viewsets

from backend.api.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
