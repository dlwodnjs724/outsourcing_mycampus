from django.db import models

class Univ(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}: {self.email}'