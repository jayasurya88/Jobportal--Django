# auth_backends/custom_auth_backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRecruiterAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.is_recruiter and user.is_approved:
                if user.check_password(password):
                    return user
            else:
                return None
        except User.DoesNotExist:
            return None
