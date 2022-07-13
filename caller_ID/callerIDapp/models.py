from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager

class SpamNumbers(models.Model):
    phone = models.CharField('Phone Number', max_length=10,unique=True,primary_key=True )
    reports = models.IntegerField()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True,null=True,blank=True)
    phone = models.CharField('Phone Number', max_length=10,unique=True,primary_key=True )
    name = models.CharField('Name', max_length=50, )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    spam = models.OneToOneField(SpamNumbers, on_delete=models.DO_NOTHING,null=True,blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name','password']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

class Phonebook(models.Model):
    class Meta:
        unique_together = (('phone', 'name'),)
    phone = models.CharField('Phone Number', max_length=10)
    name = models.CharField( max_length=50, )

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,null=True,blank=True)
