from django.db import models
import datetime
from accounts.models import User
from core.models import Univ
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from pytz import utc

class Report(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_column='content_type_id')
    object_id = models.PositiveIntegerField(db_column='object_id')
    content_object = GenericForeignKey('content_type', 'object_id')

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    what = models.TextField(max_length=500, blank=False)
    

class Category(models.Model):
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, related_name='category', blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscrp = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Category (PK: {self.pk}, Name: {self.name}, Univ: {self.univ.full_name})'


class Suggested(models.Model):
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, related_name='suggested_category', blank=False)
    name = models.CharField(max_length=30, blank=False, unique=True)
    dscrp = models.TextField(blank=False)
    suggested_at = models.DateTimeField(auto_now_add=True)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Suggested_Category: {self.name}'


class Post(models.Model):
    ctgy = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=False, null=True)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, default=0, related_name='liked', blank=True)
    views = models.PositiveIntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)

    saved = models.ManyToManyField(User, related_name='saved', blank=True)
    report = GenericRelation(Report, object_id_field='object_id', content_type_field='content_type', related_query_name='posts')


    class Meta:
        ordering = ['-created_at']

    def time_interval(self):
        now = utc.localize(datetime.datetime.utcnow())
        create = utc.localize(self.created_at)
        time_intervals = now - create
        
        return time_intervals

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Post (PK: {self.pk}, Title: {" ".join(self.title.split()[0:2])}...)'

    @property
    def name(self):
        return 'anon' if self.is_anonymous else self.author.username


def get_image_filename(instance, filename):
    id = instance.post.id
    return f'post_images/{id}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, blank=False)
    image = models.ImageField(upload_to=get_image_filename)

    def __str__(self):
        return f'Image (PK: {self.pk}, Post: {self.post.pk}, Author: {self.post.author.username})'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    content = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=True)
    comment_likes = models.ManyToManyField(User, related_name='comment_liked', blank=True)

    # 대댓글
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    report = GenericRelation(Report, object_id_field='object_id', content_type_field='content_type', related_query_name='comments')

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.comment_likes.count()

    def __str__(self):
        return f'{self.content} by {self.author}'

    @property
    def name(self):
        return 'anon' if self.is_anonymous else self.author.username

    # def __str__(self):
    #     return f'Comment (PK: {self.pk}, Author: {self.author.username} Parent: {self.parent})'

