from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from backend.api.serializers.user_serializer import UserSerializer
from backend.api.permissions import IsOwnerOrReadOnly


class CheckViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response({'authenticated': request.user.is_authenticated,
                         'user': serializer.data}, status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def list(self, request, pk=None):
        queryset = User.objects.filter()
        serializer = UserSerializer(queryset,
                                    context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user,
                                    context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.filter()
        user = get_object_or_404(queryset, pk=pk)

        self.check_object_permissions(self.request, user.profile)

        serializer = UserSerializer(user, data=request.data, partial=True,
                                    context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

        return [permission() for permission in permission_classes]
