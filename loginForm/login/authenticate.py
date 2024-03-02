from django.contrib.auth.backends import BaseBackend  # get all users authenticated list
from django.contrib.auth import get_user_model  # required to get user_id
from django.db.models import Q  # query required to find email or user


class EmailAuthentication(BaseBackend):
    # get user by user_id
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel().DoesNotExist:
            return None

    # authentication email or username
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(username__exact=username) | Q(email__exact=username)
            )
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
