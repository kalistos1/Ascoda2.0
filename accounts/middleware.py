# middleware.py
from django.shortcuts import redirect
from django.utils import timezone

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and the session has a timeout set
        if (
            request.user.is_authenticated
            and 'SESSION_IDLE_TIMEOUT' in request.session
            and not request.path_info.startswith('/auth')
        ):
            last_activity = request.session.get('last_activity', None)

            # If the last activity time is not set or exceeds the timeout, log out the user
            if (
                last_activity is None
                or (timezone.now() - last_activity).seconds > request.session['SESSION_IDLE_TIMEOUT']
            ):
                return redirect('account:signout')  # Replace with the actual URL name for the logout view

        return response