from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.dispatch import receiver
from django.utils.encoding import force_bytes, force_text

from backend.api.permissions import IsOwnerOrReadOnly
from backend.api.serializers import UserSerializer, UserCreateSerializer

from .tokens import account_activation_token

from . import SessionAuthAll


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={'request': request})
        if request.user.__str__() == 'AnonymousUser':
            return Response({'authenticated': False, 'user': {"username": 'AnonymousUser'}},
                            status.HTTP_200_OK)
        return Response({'authenticated': request.user.is_authenticated,
                         'user': serializer.data}, status.HTTP_200_OK)

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        user = authenticate(request,
                            username=request.data.get('username', None),
                            password=request.data.get('password', None))
        if user is None:
            return Response({"error": {"login": ["Invalid username or password"]}},
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'authenticated': True,
                         'user': UserSerializer(user).data},
                        status.HTTP_200_OK)


class LogOutView(APIView):
    """Logout the user"""
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        logout(request)
        response = Response({"status": "successfully logged out"},
                            status.HTTP_200_OK)
        response.delete_cookie('csrftoken')
        return response


class Register(APIView):
    """Create a new user, with email verification"""
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        current_site = get_current_site(request)
        site_name = current_site.name

        subject = loader.render_to_string(
            'auth/email_verification_subject.txt', {
                "site-name": site_name,
            })

        message = loader.render_to_string('auth/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        user.email_user(subject, message, from_email="noreply@localhost")

        return Response({
            "status": "success",
            "message": "Check email for verification"
        }, status=status.HTTP_201_CREATED)


class ConfirmEmail(APIView):
    """Logout the user"""
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    def get(self, request, format=None):
        token = request.query_params.get('token')
        uidb64 = request.query_params.get('uidb64')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return Response({
                "status": "success",
                "message": "Check email for verification"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "failure",
            "message": "Email verification Failed!"
        }, status=status.HTTP_400_BAD_REQUEST)
