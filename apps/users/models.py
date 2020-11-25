from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserModel(AbstractUser):
    # mobile = models.CharField(max_length=11)
    # password = models.CharField(verbose_name='密码', help_text='password')
    # _password = models.CharField(verbose_name='确认密码', help_text='_password')

    class Meta:
        db_table = 'auth_user'

