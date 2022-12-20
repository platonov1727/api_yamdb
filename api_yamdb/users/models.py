from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import user_regex_validator


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLES = [(USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin')]
    username = models.CharField(null=True,
                                max_length=150,
                                unique=True,
                                validators=[user_regex_validator])

    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=9, choices=USER_ROLES, default='user')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
