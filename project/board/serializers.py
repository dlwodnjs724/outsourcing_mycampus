from rest_framework import serializers, generics, pagination

from accounts.models import User
from board.models import Post, Category, Comment
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


class PostSerializer(serializers.ModelSerializer):
    ctgy = NestedCategorySerializer()
    comments = NestedCommentsSerializer(many=True)
    author = NestedUserSerializer()
    time_interval = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'
