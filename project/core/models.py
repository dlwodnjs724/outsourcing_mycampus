from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone

#accounts에서 import가 잘되지 않아 임시로
class User(AbstractUser):
    UNIV_CHOICES = ((1, 1), (2, 2), (3, 3))
    GENDER_CHOICES = (('m', "Male"), ('f', "Female"))

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # will_graduate_in = models.DateField()
    terms_acceptance = models.BooleanField(default=False)
    univ = models.CharField(max_length=20, choices=UNIV_CHOICES)

class Univ(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, related_name='category',blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscrp = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Category (PK: {self.pk}, Name: {self.name}, Univ: {self.univ.name})'

# def get_short_title(e):
#     if len(" ".join(e.split()[0:2])) > 10:
#         a = " ".join(e.split()[0:1].append("..."))
#         return str(a)
#     else:
#         a = " ".join(e.split()[0:2])
#         return str(a)

class Post(models.Model):
    ctgy = models.ForeignKey(Category, on_delete=models.CASCADE, related_name ='posts',blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='posts',blank=False)
    title = models.CharField(max_length=100,blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    likes = models.ManyToManyField(User, related_name='liked', blank=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def time_interval(self):
        now = datetime.now(timezone.utc)
        time_interval = now - self.created_at
        return time_interval

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Post (PK: {self.pk}, Title: {" ".join(self.title.split()[0:2])}... Author: {self.user.username})'

def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)  


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None,blank=False)
    image = models.ImageField(upload_to=get_image_filename)

    def __str__(self):
        return f'Image (PK: {self.pk}, Post: {self.post.pk}, Author: {self.post.user.username})'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    content = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment (PK: {self.pk}, Author: {self.author.username})'