from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(models.Model):

    number_phone = models.CharField(max_length=15, unique=True)
    activate_invite_code = models.CharField(max_length=6, unique=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.number_phone




