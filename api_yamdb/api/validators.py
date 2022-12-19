from django.core.validators import RegexValidator

user_lenght_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Имя пользователя содержит недопустимый символ')
