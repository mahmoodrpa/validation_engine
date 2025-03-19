
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils import timezone

class ExpiringPasswordBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)

        if user and not user.password_changed:
            # Check if the password has expired (24 hours in this case)
            expiration_time = user.date_joined + timezone.timedelta(hours=24)
            if timezone.now() > expiration_time:
                user.set_unusable_password()
                user.save()

        return user
