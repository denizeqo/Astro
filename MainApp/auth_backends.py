from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class MongoDBAuthBackend(ModelBackend):
    """
    Custom auth backend that skips updating last_login on login.
    django-mongodb-backend has issues with save(update_fields=...) 
    because MongoDB's _id isn't mapped to Django's pk property.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce timing difference
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            # Skip updating last_login to avoid MongoDB pk issue
            return user
        return None