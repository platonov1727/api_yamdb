from django.core.validators import RegexValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

user_regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Имя пользователя содержит недопустимый символ')
