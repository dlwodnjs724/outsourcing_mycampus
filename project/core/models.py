from django.db import models
# from models import User

class Univ(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, related_name='category',blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscrp = models.TextField(blank=False)
 
class Post(models.Model):
    ctgy = models.ForeignKey(Category, on_delete=models.CASCADE, related_name ='posts',blank=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='posts',blank=False)
    title = models.CharField(max_length=100,blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    # likes = models.ManyToManyField(User, related_name='liked', blank=True)
    is_anonymous = models.BooleanField(default=False)

def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)  


class Image(models.Model):
    post = models.ForeignKey(Post, default=None,blank=False)
    image = models.ImageField(upload_to=get_image_filename)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    content = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment (PK: {self.pk}, Author: {self.author.username})'