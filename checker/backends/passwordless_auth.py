import json
import urllib
import uuid

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from checker.models import UserType
from checker.parser.contest_parser import get_contest_api_url


def pcms_auth(pcms_login, pcms_password):
    contest_url = get_contest_api_url(pcms_login, pcms_password)
    # try:
    with urllib.request.urlopen(contest_url) as url:
        json_dictionary = json.loads(url.read().decode())
    return 'ok' in json_dictionary.keys()


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        is_pcms_auth = pcms_auth(pcms_login=username, pcms_password=password)
        print('here', kwargs.get('response'))
        userModel = get_user_model()
        try:
            user = None
            if is_pcms_auth:
                user = userModel.objects.get(username=username)
            else:
                user = userModel.objects.get(username=username)
            return user
        except userModel.DoesNotExist:
            if is_pcms_auth:
                """Returns a random string of length string_length."""
                random = str(uuid.uuid4())  # Convert UUID format to a Python string.
                random = random.upper()  # Make all characters uppercase.
                random = random.replace("-", "")  # Remove the UUID '-'.
                new_password = random[0:10]
                user = get_user_model().objects.create_user(username, password=new_password)
                user_type = UserType()
                user_type.user = user
                user_type.auth_type = 'p'
                user_type.save()
                return user
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
