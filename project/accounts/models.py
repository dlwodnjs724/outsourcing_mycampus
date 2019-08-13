from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    UNIV_CHOICES = ((1, 1), (2, 2), (3, 3))
    GENDER_CHOICES = (('m', "Male"), ('f', "Female"))

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    will_graduate_in = models.DateField()
    terms_acceptance = models.BooleanField(default=False)
    univ = models.CharField(max_length=20, choices=UNIV_CHOICES)