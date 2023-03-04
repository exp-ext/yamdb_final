import re

from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


@deconstructible
class UsernameValidator:
    """Проверка username на паттерн: буквы/цифры/_/-."""

    message = _('Разрешены только буквы/цифры/_/- '
                'Использовать "me" в качестве username запрещено.')
    code = 'invalid'
    user_regex = re.compile(r"^[\w-]+$")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if value.lower() == 'me':
            raise ValidationError(self.message, code=self.code)

        if not self.user_regex.match(value):
            raise ValidationError(self.message, code=self.code)


validate_username = UsernameValidator()
