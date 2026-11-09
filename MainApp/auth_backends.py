from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login

# Disconnect the signal that updates last_login on login.
# django-mongodb-backend cannot handle save(update_fields=...) with no pk,
# causing "Cannot force an update in save() with no primary key".
user_logged_in.disconnect(update_last_login)


class MongoDBAuthBackend(ModelBackend):
    """
    Custom auth backend for MongoDB compatibility.
    Disconnects last_login update signal and ensures pk is set from _id.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            # Ensure pk is set from MongoDB _id for session storage
            if user.pk is None:
                if hasattr(user, '_id') and user._id is not None:
                    user.id = user._id
            return user
        return None