from django.db import models


class Univ(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="univ/logo/", blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.domain}'
