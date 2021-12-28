from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.search import *


# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password, school):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            school=school,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
         )

        user.is_active = True
        user.is_contributor = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    school = models.CharField(max_length=30, unique=False, default="EPITA")
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    object = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def in_School(self, school):
        if (((self.email).split('@'))[1]) == "hyperion.tf":
            return True
        return self.school == school

