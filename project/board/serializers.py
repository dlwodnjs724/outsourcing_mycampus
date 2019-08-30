from rest_framework import serializers, generics, pagination

from accounts.models import User
from board.models import Post, Category, Comment, Image, Noti
from core.models import Univ


class NestedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author',)


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class NestedCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('univ', 'name')


class NestedImageSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Image
        fields = ('image', 'image_thumbnail')


class PostSerializer(serializers.ModelSerializer):
    ctgy = NestedCategorySerializer()
    comments = NestedCommentsSerializer(many=True)
    author = NestedUserSerializer()
    time_interval = serializers.ReadOnlyField()
    images = NestedImageSerializer(many=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'


class NotiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noti
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'
