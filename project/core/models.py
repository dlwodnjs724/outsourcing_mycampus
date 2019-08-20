from django.db import models

class Univ(models.Model):
    full_name = models.CharField(max_length=50)
    domain = models.CharField(max_length=20)        # univ email address(@ 뒤에)
    url_name = models.CharField(max_length=10)      # url parameter name
    short_name = models.CharField(max_length=10)    # 대학 약자(header 에 표기)
    logo = models.ImageField(upload_to="univ/logo/", blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.full_name}: {self.domain}'


# class Report(models.Model):
#     reported_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     reported_by = models.ForeignKey(User, on_delete=models.SET_NULL)

#     what = models.TextField(max_length=500, blank=False)
    