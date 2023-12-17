import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False):
        if not email or not password:
            raise TypeError('Users must have both email and password.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = is_staff
        user.save()
        return user

    def create_superuser(self, email, password):
        if not email or not password:
            raise TypeError('Users must have both email and password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    last_name = models.CharField(max_length=255, default=None, null=True)
    middle_name = models.CharField(max_length=255, default=None, null=True)
    first_name = models.CharField(max_length=255, default=None, null=True)

    birthday = models.DateField(null=True)
    insurance_policy_number = models.CharField(max_length=16, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        if not self.last_name:
            return self.email
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_short_name(self):
        if not self.last_name:
            return self.email
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token
