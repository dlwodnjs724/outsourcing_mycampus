from django import forms
from django.db import models
import datetime
from accounts.models import User
from core.models import Univ
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from pytz import utc
import arrow
import math
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


class Noti(models.Model):
    NOTI_CHOICES = (
        ('c_l', 'comment_like'),
        ('c_c', 'nest_comment'),
        ('c','comment'),
        ('p_l','post_like')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_column='content_type_id')
    object_id = models.PositiveIntegerField(db_column='object_id')
    content_object = GenericForeignKey('content_type', 'object_id')
    from_n = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="_from")
    to_n = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="_to")
    noti_type = models.CharField(max_length=5, choices=NOTI_CHOICES, null=True)
    is_read = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def time_interval(self):
        now = arrow.now().timestamp
        # now = utc.localize(datetime.datetime.utcnow())
        create = self.created_at.timestamp()
        ti = math.floor(int(now - create) / 60)

        if ti < 60:
            t = f'{ti}m'
        elif 60 <= ti < (24 * 60):
            t = f'{math.floor(ti / 60)}h'
        else:
            t = f'{math.floor(ti / (24 * 60))}d'
        return t

    def get_context(self):
        tn = ""
        notiType = self.noti_type
        if notiType == "c_l":
            tn = "likes your comment."
        elif notiType == "c_c":
            tn = "commented on your comment."
        elif notiType == "c":
            tn = "commented on your post."
        elif notiType == "p_l":
            tn = "likes your post."
        return tn

    def get_category(self):
        q = ""
        content = self.content_type
        if str(content) == "post":
            q = Post.objects.select_related('ctgy').get(pk=self.object_id).ctgy.name
        elif str(content) == "comment":
            q = Comment.objects.select_related('post', 'post__ctgy').get(pk=self.object_id).post.ctgy.name
        return q

    def get_post(self):
        q = ""
        content = self.content_type
        if str(content) == "post":
            q = self.object_id
        elif str(content) == "comment":
            q = Comment.objects.select_related('post').get(pk=self.object_id).post.pk
        return q


class Report(models.Model):
    TYPE_CHOICES = (
        ('sexual', 'Sexual insult'),
        ('bully', 'Cyber bullying'),
        ('racist', 'Racist remarks'),
        ('illegal', 'Illegal activity'),
        ('others', 'Others')
    )

    TARGET_CHOICES = (
        ('c', 'comment'),
        ('p', 'post')
    )

    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)
    target_type = models.CharField(max_length=5, choices=TARGET_CHOICES, null=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reporting', null=True)
    abuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported',null=True)
    target_content = models.OneToOneField('ReportedContent', on_delete=models.PROTECT, related_name='report_paper',null=True)

    accepted = models.BooleanField(default=False, null=True)
    is_handled = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ReportedContent(models.Model):
    origin_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, related_name='reported_copy', null=True, blank=True)
    origin_post = models.ForeignKey('Post', on_delete=models.SET_NULL, related_name='reported_copy', null=True, blank=True)
    content = models.TextField(blank=False, null=False)
    title = models.CharField(max_length=100, null=True)


class Category(models.Model):
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, related_name='category', blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscrp = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):

        return self.name


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
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, default=0, related_name='liked', blank=True)
    views = models.PositiveIntegerField(default=0)
    viewed_by = models.ManyToManyField(User, related_name='viewed', blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_notice = models.BooleanField(default=False)
    is_ctgy_notice = models.BooleanField(default=False)

    saved = models.ManyToManyField(User, related_name='saved', blank=True)

    is_reported = models.BooleanField(default=False)
    noti = GenericRelation(Noti, object_id_field='object_id', content_type_field='content_type', related_query_name='posts')

    class Meta:
        ordering = ['-created_at']

    @property
    def time_interval(self):
        now = arrow.now().timestamp
        # now = utc.localize(datetime.datetime.utcnow())
        create = self.created_at.timestamp()
        ti = math.floor(int(now - create) / 60)

        if ti < 60:
            t = f'{ti}m'
        elif 60 <= ti < (24 * 60):
            t = f'{math.floor(ti / 60)}h'
        else:
            t = f'{math.floor(ti / (24 * 60))}d'
        return t

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Post (PK: {self.pk}, Title: {" ".join(self.title.split()[0:2])}...)'

    @property
    def name(self):
        return 'anon' if self.is_anonymous else self.author.username


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, blank=False, related_name="images")
    image = models.ImageField(upload_to='board/post/images/')
    image_thumbnail = ImageSpecField(
        source='image',  # 원본 ImageField 명
        processors=[Thumbnail(200, 200)],  # 처리할 작업목록
        format='JPEG',  # 최종 저장 포맷
        options={'quality': 60})

    def __str__(self):
        return f'Image (PK: {self.pk}, Post: {self.post.pk}, Author: {self.post.author.username})'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    content = models.CharField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=True)
    comment_likes = models.ManyToManyField(User, related_name='comment_liked', blank=True)

    # 대댓글
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    noti = GenericRelation(Noti, object_id_field='object_id', content_type_field='content_type', related_query_name='comments')

    class Meta:
        ordering = ['-created_at']

    @property
    def time_interval(self):
        now = arrow.now().timestamp
        # now = utc.localize(datetime.datetime.utcnow())
        create = self.created_at.timestamp()
        ti = math.floor(int(now - create) / 60)

        if ti < 60:
            t = f'{ti}m'
        elif 60 <= ti < (24 * 60):
            t = f'{math.floor(ti / 60)}h'
        else:
            t = f'{math.floor(ti / (24 * 60))}d'
        return t

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def name(self):
        if self.is_anonymous:
            if self.author == self.post.author:
                return 'anon(OP)'
            return 'anon'
        return self.author.username

    def children(self):
        return Comment.objects.prefetch_related('comment_likes')\
            .select_related('author', 'parent', 'post', 'post__author')\
            .filter(parent=self)

    def total_likes(self):
        return self.comment_likes.count()

    def __str__(self):
        return f'{self.content} by {self.author}'
