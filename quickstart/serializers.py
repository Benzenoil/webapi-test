from rest_framework import serializers
from .models import Snippet, User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'nickname', 'password')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'comment')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'nickname', 'comment')


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
