from rest_framework.authentication import SessionAuthentication


class SessionAuthAll(SessionAuthentication):

    def authenticate(self, request):
        """
        Returns a `User` and force CSRF even if
        the user is Unauthenticated
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)
