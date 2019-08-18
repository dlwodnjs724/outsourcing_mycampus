from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Univ


class User(AbstractUser):
    GENDER_CHOICES = (
        ('f', "Female"),
        ('m', "Male"),
        ('o', 'Other')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    class_of = models.IntegerField(null=True)
    terms_acceptance = models.BooleanField(default=False)
    univ = models.ForeignKey(Univ, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()

    is_validate = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)