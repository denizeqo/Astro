from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# Patch User.save() to handle MongoDB pk compatibility.
# django-mongodb-backend stores _id as MongoDB ObjectId; Django's pk may be None,
# causing "Cannot force an update in save() with no primary key" during login.
User = get_user_model()
_original_save = User.save


def _patched_save(self, *args, **kwargs):
    # Ensure pk is set from MongoDB _id
    if self.pk is None:
        if hasattr(self, '_id') and self._id is not None:
            self.id = self._id
    # Remove force_update to avoid MongoDB incompatibility
    kwargs.pop('force_update', None)
    return _original_save(self, *args, **kwargs)


User.save = _patched_save


class MongoDBAuthBackend(ModelBackend):
    """
    Custom auth backend for MongoDB compatibility.
    Skips updating last_login to avoid save() issues with django-mongodb-backend.
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
            # Ensure pk is set for session storage
            if user.pk is None:
                if hasattr(user, '_id') and user._id is not None:
                    user.id = user._id
            return user
        return None