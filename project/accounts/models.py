from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Univ


class User(AbstractUser):
    GENDER_CHOICES = (
        ('f', "Female"),
        ('m', "Male"),
        ('o', 'Other')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)
    class_of = models.IntegerField(null=True, blank=False)
    terms_acceptance = models.BooleanField(default=False, blank=False)
    univ = models.ForeignKey(Univ, on_delete=models.SET_NULL, null=True, blank=False)
    email = models.EmailField(blank=False, null=False)

    is_validated = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def user_likes_this(self, post):
        pass