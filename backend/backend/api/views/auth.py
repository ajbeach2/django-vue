from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.api.serializers import UserSerializer


class SessionAuthAll(SessionAuthentication):
    def authenticate(self, request):
        """
        Returns a `User` and force CSRF even if
        the user is Unauthenticated
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, "user", None)

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={"request": request})
        if request.user.__str__() == "AnonymousUser":
            return Response(
                {"authenticated": False, "user": {"username": "AnonymousUser"}},
                status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "authenticated": request.user.is_authenticated,
                    "user": serializer.data,
                },
                status.HTTP_200_OK,
            )

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        user = authenticate(
            request,
            username=request.data.get("username", None),
            password=request.data.get("password", None),
        )
        if user is None:
            return Response(
                {"error": {"login": ["Invalid username or password"]}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            login(request, user)
            return Response(
                {"authenticated": True, "user": UserSerializer(user).data},
                status.HTTP_200_OK,
            )


class LogOutView(APIView):
    permission_classes = ()
    authentication_classes = (SessionAuthAll,)

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        logout(request)
        response = Response({"status": "successfully logged out"}, status.HTTP_200_OK)
        response.delete_cookie("csrftoken")
        return response
